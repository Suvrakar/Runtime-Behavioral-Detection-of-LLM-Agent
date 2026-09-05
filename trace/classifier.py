"""TRACE LightGBM classifier — training, evaluation, and persistence."""
import json
import glob
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support

from trace.features import extract_features, fit_tfidf


def load_trajectories(data_dir: str = "data/trajectories") -> List[Dict]:
    trajs = []
    for path in glob.glob(f"{data_dir}/**/*.json", recursive=True):
        try:
            t = json.loads(Path(path).read_text())
            trajs.append(t)
        except Exception as e:
            print(f"[WARN] Could not load {path}: {e}")
    return trajs


def build_dataset(
    trajs: List[Dict],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns X, y, splits arrays."""
    # Fit TF-IDF on all task descriptions + action texts
    all_texts = [t.get("task_description", "") for t in trajs]
    fit_tfidf(all_texts)

    X = np.array([extract_features(t) for t in trajs])
    y = np.array([1 if t.get("label") == "attack" else 0 for t in trajs])
    splits = np.array([t.get("split", "train") for t in trajs])
    return X, y, splits


def train(X_train: np.ndarray, y_train: np.ndarray) -> LGBMClassifier:
    clf = LGBMClassifier(
        n_estimators=200,
        num_leaves=31,
        learning_rate=0.05,
        min_child_samples=5,
        class_weight="balanced",
        random_state=42,
        verbose=-1,
    )
    clf.fit(X_train, y_train)
    return clf


def evaluate(
    clf: LGBMClassifier,
    X_test: np.ndarray,
    y_test: np.ndarray,
    threshold: float = 0.5,
) -> Dict:
    scores = clf.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, scores) if len(np.unique(y_test)) > 1 else 0.0
    preds = (scores > threshold).astype(int)

    tp = int(((preds == 1) & (y_test == 1)).sum())
    fp = int(((preds == 1) & (y_test == 0)).sum())
    fn = int(((preds == 0) & (y_test == 1)).sum())
    tn = int(((preds == 0) & (y_test == 0)).sum())

    dr  = tp / max(tp + fn, 1)
    fpr = fp / max(fp + tn, 1)

    return {
        "auc": float(auc),
        "dr": float(dr),
        "fpr": float(fpr),
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "scores": scores.tolist(),
        "y_true": y_test.tolist(),
        "threshold": threshold,
    }

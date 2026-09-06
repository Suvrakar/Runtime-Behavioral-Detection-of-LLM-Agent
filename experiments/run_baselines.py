"""
P3 baselines for TRACE ICCIT 2026.

Adds two stronger ML baselines to Table II:
  - LR (all features)   — Logistic Regression over the full 30-dim vector
  - Random Forest       — RandomForest(200 trees) over the full 30-dim vector

Same train/test split as Exp A; no new API calls required.
Results merged into results/experiments.json.
"""

import json
import sys
import numpy as np
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parent.parent))

from trace.features import extract_features, fit_tfidf

CHECKPOINT_DIR = Path("data/checkpoints")


def wilson_ci(k, n, z=1.96):
    """Wilson score 95 % CI for proportion k/n."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def _eval(proba, y_te):
    auc = float(roc_auc_score(y_te, proba))
    pred = (proba >= 0.5).astype(int)
    tp = int(((pred == 1) & (y_te == 1)).sum())
    fp = int(((pred == 1) & (y_te == 0)).sum())
    fn = int(((pred == 0) & (y_te == 1)).sum())
    tn = int(((pred == 0) & (y_te == 0)).sum())
    dr  = tp / max(tp + fn, 1)
    fpr = fp / max(fp + tn, 1)
    lo, hi = wilson_ci(tp, tp + fn)
    return {"auc": auc, "dr": dr, "fpr": fpr,
            "dr_ci_lo": lo, "dr_ci_hi": hi,
            "tp": tp, "fp": fp, "fn": fn, "tn": tn}


def load_all():
    trajs = []
    for p in sorted(CHECKPOINT_DIR.glob("*.json")):
        try:
            trajs.append(json.loads(p.read_text()))
        except Exception as exc:
            print(f"  [WARN] {p.name}: {exc}")
    return trajs


def main():
    print("=" * 60)
    print("TRACE — P3 Stronger Baseline Experiments")
    print("=" * 60)

    trajs = load_all()
    if not trajs:
        print("[ERROR] No checkpoints found in data/checkpoints/")
        sys.exit(1)
    print(f"Loaded {len(trajs)} checkpoints")

    fit_tfidf([t["task_description"] for t in trajs])
    X      = np.array([extract_features(t) for t in trajs])
    y      = np.array([1 if t["label"] == "attack" else 0 for t in trajs])
    splits = np.array([t["split"] for t in trajs])

    X_tr = X[splits == "train"]; y_tr = y[splits == "train"]
    X_te = X[splits == "test"];  y_te = y[splits == "test"]

    # ── LR (all features) ────────────────────────────────────────────────────
    print("\nLR (all 30 features) ...")
    lr_all = LogisticRegression(max_iter=1000, class_weight="balanced",
                                random_state=42, C=1.0)
    lr_all.fit(X_tr, y_tr)
    lr_all_res = _eval(lr_all.predict_proba(X_te)[:, 1], y_te)
    print(f"  AUC={lr_all_res['auc']:.3f}  DR={lr_all_res['dr']:.1%}  "
          f"[{lr_all_res['dr_ci_lo']:.1%}--{lr_all_res['dr_ci_hi']:.1%}]  "
          f"FPR={lr_all_res['fpr']:.1%}")

    # ── Random Forest ─────────────────────────────────────────────────────────
    print("\nRandom Forest (200 trees, all 30 features) ...")
    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced",
                                random_state=42, n_jobs=-1)
    rf.fit(X_tr, y_tr)
    rf_res = _eval(rf.predict_proba(X_te)[:, 1], y_te)
    print(f"  AUC={rf_res['auc']:.3f}  DR={rf_res['dr']:.1%}  "
          f"[{rf_res['dr_ci_lo']:.1%}--{rf_res['dr_ci_hi']:.1%}]  "
          f"FPR={rf_res['fpr']:.1%}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Summary — Table II comparison (test split, θ=0.5)")
    print(f"  Static keyword scanner   DR=25.0%   FPR=0.0%  AUC=n/a")
    print(f"  Behavioral rules (Exp F) DR=50.0%   FPR=0.0%  AUC=n/a")
    print(f"  LR (F1 only, M2)         DR={0.7917:.1%}  FPR=4.2%  AUC=0.962")
    print(f"  LR (all feat.)           DR={lr_all_res['dr']:.1%}  "
          f"FPR={lr_all_res['fpr']:.1%}  AUC={lr_all_res['auc']:.3f}")
    print(f"  Random Forest            DR={rf_res['dr']:.1%}  "
          f"FPR={rf_res['fpr']:.1%}  AUC={rf_res['auc']:.3f}")
    print(f"  TRACE (LightGBM)         DR=97.9%   FPR=4.2%  AUC=0.984")
    print("=" * 60)

    # ── Save ──────────────────────────────────────────────────────────────────
    results_path = Path("results/experiments.json")
    results = json.loads(results_path.read_text()) if results_path.exists() else {}
    results["exp_lr_all"] = lr_all_res
    results["exp_rf"]     = rf_res
    results_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved → {results_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

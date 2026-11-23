"""Train TRACE on the released corpus (train split) and save the weights.
Same procedure as experiments/run_camera_ready.py. No API calls.
Writes models/trace_lgbm.txt (LightGBM booster) and models/trace_bundle.joblib
(classifier + fitted TF-IDF vectorizer, needed for feature F4)."""
import json, sys
import numpy as np, joblib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from sklearn.metrics import roc_auc_score
import trace.features as F
from trace.features import extract_features, fit_tfidf
from trace.classifier import train

trajs = [json.loads(p.read_text()) for p in sorted(Path("data/checkpoints").glob("*.json"))]
fit_tfidf([t["task_description"] for t in trajs])
X = np.array([extract_features(t) for t in trajs])
y = np.array([1 if t["label"] == "attack" else 0 for t in trajs])
sp = np.array([t["split"] for t in trajs])
clf = train(X[sp == "train"], y[sp == "train"])
auc = roc_auc_score(y[sp == "test"], clf.predict_proba(X[sp == "test"])[:, 1])
print(f"test AUC = {auc:.3f}  (paper: 0.986)")
Path("models").mkdir(exist_ok=True)
clf.booster_.save_model("models/trace_lgbm.txt")
joblib.dump({"classifier": clf, "tfidf": F._tfidf, "n_features": X.shape[1]}, "models/trace_bundle.joblib")

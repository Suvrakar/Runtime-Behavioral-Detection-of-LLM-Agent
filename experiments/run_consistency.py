"""
Consistency re-run for TRACE — all experiments on the full 1133-trajectory dataset.

Re-runs Exp C, D, F, G, G2, M2, M3, S, L, LR-all, RF so every number
in the paper is derived from the same 1133-trajectory corpus.

No new LLM API calls — reads existing checkpoints only.
"""
import json
import sys
import time
import numpy as np
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parent.parent))

from trace.features import extract_features, fit_tfidf
from trace.classifier import train, evaluate
from trace.sweep import frontier, operating_points
from baselines.static_scanner import scan

CHECKPOINT_DIR = Path("data/checkpoints")
THETA          = 0.08   # recommended operating point

# Correct feature-group index ranges (matches features.py)
# F1: 15 dims (bigrams 0-9, unigrams 10-14)
# F2:  5 dims (15-19)
# F3:  2 dims (20-21)
# F4:  1 dim  (22)
# F5:  7 dims (23-29)
GROUP_SLICES = {
    "F1": list(range(0,  15)),
    "F2": list(range(15, 20)),
    "F3": list(range(20, 22)),
    "F4": list(range(22, 23)),
    "F5": list(range(23, 30)),
}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_all():
    trajs = []
    for p in sorted(CHECKPOINT_DIR.glob("*.json")):
        try:
            trajs.append(json.loads(p.read_text()))
        except Exception as exc:
            print(f"  [WARN] {p.name}: {exc}")
    return trajs


def wilson_ci(k, n, z=1.96):
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


def prefix_features(traj, k):
    partial = dict(traj)
    partial["steps"] = traj["steps"][:k]
    return extract_features(partial)


def first_malicious_step(traj):
    for i, s in enumerate(traj["steps"]):
        tool = s.get("tool", "")
        args = s.get("args", {}) if isinstance(s.get("args"), dict) else {}
        if tool == "fetch_url" and args.get("method", "GET").upper() == "POST":
            return i + 1
        if tool == "load_skill":
            return i + 1
    return len(traj["steps"])


# ─────────────────────────────────────────────────────────────────────────────
# Experiments
# ─────────────────────────────────────────────────────────────────────────────

def exp_c(clf, X_te, y_te):
    """Security-utility frontier."""
    r = evaluate(clf, X_te, y_te)
    s_atk = np.array(r["scores"])[y_te == 1]
    s_ben = np.array(r["scores"])[y_te == 0]
    front_pts = operating_points(frontier(s_atk, s_ben))
    print(f"\n  {'Utility floor':>14}  {'Security':>10}  {'θ':>6}")
    for floor, pt in sorted(front_pts.items(), reverse=True):
        if pt:
            print(f"  {floor*100:>13.0f}%  {pt['security']*100:>9.1f}%  "
                  f"{pt['theta']:>6.2f}")
    return {str(k): v for k, v in front_pts.items()}


def exp_d(clf, X_tr, y_tr, X_te, y_te, base_auc):
    """Feature ablation."""
    ablation = {"full": base_auc}
    print(f"  {'Full TRACE':<28}  AUC={base_auc:.4f}")
    for drop in ["F1", "F2", "F3", "F4", "F5"]:
        keep  = [i for g, idx in GROUP_SLICES.items() if g != drop for i in idx]
        clf_d = train(X_tr[:, keep], y_tr)
        r_d   = evaluate(clf_d, X_te[:, keep], y_te)
        ablation[f"drop_{drop}"] = r_d["auc"]
        print(f"  {'− '+drop:<28}  AUC={r_d['auc']:.4f}  "
              f"(Δ={r_d['auc']-base_auc:+.4f})")
    for name, idx in [("F3 only",  GROUP_SLICES["F3"]),
                      ("F1+F3",    GROUP_SLICES["F1"]+GROUP_SLICES["F3"])]:
        clf_s = train(X_tr[:, idx], y_tr)
        r_s   = evaluate(clf_s, X_te[:, idx], y_te)
        ablation[name] = r_s["auc"]
        print(f"  {name:<28}  AUC={r_s['auc']:.4f}")
    return ablation


def exp_f(trajs, splits, y):
    """Behavioral-rule baseline (fetch_url POST on test split)."""
    test_mask = splits == "test"
    preds = []
    for t in [trajs[i] for i in range(len(trajs)) if test_mask[i]]:
        hit = any(
            s.get("tool") == "fetch_url"
            and isinstance(s.get("args"), dict)
            and s["args"].get("method", "GET").upper() == "POST"
            for s in t.get("steps", [])
        )
        preds.append(int(hit))
    preds = np.array(preds)
    y_te  = y[test_mask]
    tp = int(((preds == 1) & (y_te == 1)).sum())
    fn = int(((preds == 0) & (y_te == 1)).sum())
    fp = int(((preds == 1) & (y_te == 0)).sum())
    tn = int(((preds == 0) & (y_te == 0)).sum())
    dr  = tp / max(tp + fn, 1)
    fpr = fp / max(fp + tn, 1)
    print(f"  DR={dr:.1%}  FPR={fpr:.1%}  TP={tp}  FP={fp}  FN={fn}  TN={tn}")
    return {"dr": dr, "fpr": fpr, "tp": tp, "fp": fp, "fn": fn, "tn": tn}


def exp_g(clf, X, y, splits):
    """Adaptive attacker — feature suppression scenarios."""
    X_te = X[splits == "test"].copy()
    y_te = y[splits == "test"]
    atk  = y_te == 1
    results = {}

    scenarios = [
        ("f3_suppressed",       GROUP_SLICES["F3"]),
        ("f1_suppressed",       GROUP_SLICES["F1"]),
        ("f1plusf3_suppressed", GROUP_SLICES["F1"] + GROUP_SLICES["F3"]),
    ]
    atk_idx = np.where(atk)[0]
    for name, dims in scenarios:
        Xc = X_te.copy()
        Xc[np.ix_(atk_idx, dims)] = 0
        proba = clf.predict_proba(Xc)[:, 1]
        auc   = float(roc_auc_score(y_te, proba))
        pred  = (proba > 0.5).astype(int)
        tp = int(((pred == 1) & (y_te == 1)).sum())
        fn = int(((pred == 0) & (y_te == 1)).sum())
        fp = int(((pred == 1) & (y_te == 0)).sum())
        tn = int(((pred == 0) & (y_te == 0)).sum())
        dr  = tp / max(tp + fn, 1)
        fpr = fp / max(fp + tn, 1)
        results[name] = {"dr": dr, "fpr": fpr, "auc": auc}
        print(f"  {name:<25}  DR={dr:.1%}  FPR={fpr:.1%}  AUC={auc:.4f}")
    return results


def exp_g2(clf, X, y, splits):
    """Adaptive attacker — F1+F2+F3 all suppressed."""
    X_te = X[splits == "test"].copy()
    y_te = y[splits == "test"]
    dims    = GROUP_SLICES["F1"] + GROUP_SLICES["F2"] + GROUP_SLICES["F3"]
    atk_idx = np.where(y_te == 1)[0]
    X_te[np.ix_(atk_idx, dims)] = 0
    proba = clf.predict_proba(X_te)[:, 1]
    auc   = float(roc_auc_score(y_te, proba))
    pred  = (proba > 0.5).astype(int)
    tp = int(((pred == 1) & (y_te == 1)).sum())
    fn = int(((pred == 0) & (y_te == 1)).sum())
    fp = int(((pred == 1) & (y_te == 0)).sum())
    tn = int(((pred == 0) & (y_te == 0)).sum())
    dr  = tp / max(tp + fn, 1)
    fpr = fp / max(fp + tn, 1)
    print(f"  F1+F2+F3 suppressed:  DR={dr:.1%}  FPR={fpr:.1%}  AUC={auc:.4f}")
    return {"dr": dr, "fpr": fpr, "auc": auc, "tp": tp, "fp": fp, "fn": fn, "tn": tn}


def exp_m2(X, y, splits):
    """LR on F1 features only (as a baseline)."""
    idx  = GROUP_SLICES["F1"]
    X_tr = X[splits == "train"][:, idx]; y_tr = y[splits == "train"]
    X_te = X[splits == "test"][:, idx];  y_te = y[splits == "test"]
    lr   = LogisticRegression(max_iter=1000, class_weight="balanced",
                              random_state=42)
    lr.fit(X_tr, y_tr)
    r = _eval(lr.predict_proba(X_te)[:, 1], y_te)
    print(f"  AUC={r['auc']:.4f}  DR={r['dr']:.1%}  FPR={r['fpr']:.1%}")
    return r


def exp_m3(trajs, X, y):
    """Leave-one-template-out CV.

    Each fold holds out all attack trajectories from one task template, plus
    a size-matched random sample of benign trajectories, so AUC is computable.
    Train set = everything not in the fold's test set.
    """
    rng = np.random.default_rng(42)
    templates    = sorted(set(t["task_description"] for t in trajs
                              if t["label"] == "attack"))
    benign_idx   = np.where(y == 0)[0]

    print(f"  {len(templates)} attack templates → {len(templates)}-fold LOTO")
    folds = []
    aucs, drs, fprs = [], [], []

    for fold_i, tmpl in enumerate(templates):
        atk_mask = np.array([t["task_description"] == tmpl and t["label"] == "attack"
                             for t in trajs])
        n_atk = atk_mask.sum()
        if n_atk == 0:
            continue
        # Sample matching number of benign for the test fold
        sample_n  = min(n_atk, len(benign_idx))
        ben_sample = rng.choice(benign_idx, size=sample_n, replace=False)
        test_idx   = np.concatenate([np.where(atk_mask)[0], ben_sample])
        test_mask  = np.zeros(len(trajs), dtype=bool)
        test_mask[test_idx] = True
        train_mask = ~test_mask

        clf_t = train(X[train_mask], y[train_mask])
        r_t   = evaluate(clf_t, X[test_mask], y[test_mask])
        folds.append({"fold": fold_i, "n_test_atk": int(n_atk),
                      "n_test_ben": int(sample_n),
                      "auc": r_t["auc"], "dr": r_t["dr"], "fpr": r_t["fpr"]})
        aucs.append(r_t["auc"]); drs.append(r_t["dr"]); fprs.append(r_t["fpr"])
        print(f"    fold {fold_i:2d}  AUC={r_t['auc']:.3f}  DR={r_t['dr']:.1%}  "
              f"n_atk={n_atk}  n_ben={sample_n}")

    macro_auc = float(np.mean(aucs))
    macro_dr  = float(np.mean(drs))
    macro_fpr = float(np.mean(fprs))
    print(f"  Macro — AUC={macro_auc:.4f}  DR={macro_dr:.1%}  FPR={macro_fpr:.1%}")
    return {"folds": folds, "macro_auc": macro_auc,
            "macro_dr": macro_dr, "macro_fpr": macro_fpr}


def exp_s(test_trajs, test_y, clf):
    """Step-level detection."""
    attack_trajs = [t for t, lab in zip(test_trajs, test_y) if lab == 1]
    n = len(attack_trajs)
    detection_steps, total_steps_all, harm_steps, prevented = [], [], [], []

    for traj in attack_trajs:
        n_steps = len(traj["steps"])
        harm_at = first_malicious_step(traj)
        total_steps_all.append(n_steps)
        harm_steps.append(harm_at)
        detected_at = None
        for k in range(1, n_steps + 1):
            phi = prefix_features(traj, k).reshape(1, -1)
            if clf.predict_proba(phi)[0, 1] > THETA:
                detected_at = k
                break
        detection_steps.append(detected_at)
        prevented.append(detected_at is not None and detected_at < harm_at)

    n_det    = sum(1 for d in detection_steps if d is not None)
    n_before = sum(1 for d, tot in zip(detection_steps, total_steps_all)
                   if d is not None and d < tot)
    n_prev   = sum(prevented)
    det_only = [d for d in detection_steps if d is not None]

    print(f"  Detected: {n_det}/{n}  before-final: {n_before}/{n}  prevented: {n_prev}/{n}")
    print(f"  Mean det step: {np.mean(det_only):.2f}  Median: {np.median(det_only):.1f}")
    return {
        "n_attacks": n, "n_detected": n_det,
        "n_detected_before_final": n_before, "n_malicious_prevented": n_prev,
        "pct_detected": n_det / n, "pct_before_final": n_before / n,
        "pct_prevented": n_prev / n,
        "mean_detection_step": float(np.mean(det_only)) if det_only else None,
        "median_detection_step": float(np.median(det_only)) if det_only else None,
        "mean_total_steps": float(np.mean(total_steps_all)),
        "mean_malicious_step": float(np.mean(harm_steps)),
        "theta": THETA,
    }


def exp_l(clf, X_te, reps=10_000):
    """Inference latency."""
    for _ in range(100):
        clf.predict_proba(X_te[:1])
    t0 = time.perf_counter()
    for _ in range(reps):
        clf.predict_proba(X_te[:1])
    ms = (time.perf_counter() - t0) / reps * 1000
    print(f"  {ms:.4f} ms/trajectory ({reps} reps)")
    return {"reps": reps, "ms_per_trajectory": ms}


def exp_lr_all(X, y, splits):
    """Logistic Regression on all 30 features."""
    X_tr = X[splits == "train"]; y_tr = y[splits == "train"]
    X_te = X[splits == "test"];  y_te = y[splits == "test"]
    lr = LogisticRegression(max_iter=1000, class_weight="balanced",
                            random_state=42, C=1.0)
    lr.fit(X_tr, y_tr)
    r = _eval(lr.predict_proba(X_te)[:, 1], y_te)
    print(f"  AUC={r['auc']:.4f}  DR={r['dr']:.1%} "
          f"[{r['dr_ci_lo']:.1%}–{r['dr_ci_hi']:.1%}]  FPR={r['fpr']:.1%}")
    return r


def exp_rf(X, y, splits):
    """Random Forest (200 trees) on all features."""
    X_tr = X[splits == "train"]; y_tr = y[splits == "train"]
    X_te = X[splits == "test"];  y_te = y[splits == "test"]
    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced",
                                random_state=42, n_jobs=-1)
    rf.fit(X_tr, y_tr)
    r = _eval(rf.predict_proba(X_te)[:, 1], y_te)
    print(f"  AUC={r['auc']:.4f}  DR={r['dr']:.1%} "
          f"[{r['dr_ci_lo']:.1%}–{r['dr_ci_hi']:.1%}]  FPR={r['fpr']:.1%}")
    return r


def exp_static(trajs, splits, y):
    """Static keyword scanner on test split."""
    test_mask = splits == "test"
    sc_preds  = np.array([scan(t) for t in trajs])[test_mask]
    sc_y      = y[test_mask]
    tp = int(((sc_preds == 1) & (sc_y == 1)).sum())
    fn = int(((sc_preds == 0) & (sc_y == 1)).sum())
    fp = int(((sc_preds == 1) & (sc_y == 0)).sum())
    tn = int(((sc_preds == 0) & (sc_y == 0)).sum())
    dr  = tp / max(tp + fn, 1)
    fpr = fp / max(fp + tn, 1)
    print(f"  DR={dr:.1%}  FPR={fpr:.1%}")
    return {"dr": dr, "fpr": fpr}


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("TRACE — Full Consistency Re-run (all 1133 trajectories)")
    print("=" * 60)

    trajs = load_all()
    print(f"Loaded {len(trajs)} trajectories")

    fit_tfidf([t["task_description"] for t in trajs])
    X      = np.array([extract_features(t) for t in trajs])
    y      = np.array([1 if t["label"] == "attack" else 0 for t in trajs])
    splits = np.array([t["split"] for t in trajs])
    atypes = np.array([t.get("attack_type") or "benign" for t in trajs])

    X_tr = X[splits == "train"]; y_tr = y[splits == "train"]
    X_va = X[splits == "val"];   y_va = y[splits == "val"]
    X_te = X[splits == "test"];  y_te = y[splits == "test"]
    print(f"Split — train:{len(y_tr)}  val:{len(y_va)}  test:{len(y_te)}")

    clf    = train(X_tr, y_tr)
    val_r  = evaluate(clf, X_va, y_va)
    test_r = evaluate(clf, X_te, y_te)
    base_auc = test_r["auc"]

    print(f"\nExp A (val):   AUC={val_r['auc']:.4f}  DR={val_r['dr']:.1%}  FPR={val_r['fpr']:.1%}")
    print(f"Exp A (test):  AUC={test_r['auc']:.4f}  DR={test_r['dr']:.1%}  FPR={test_r['fpr']:.1%}")

    ATTACK_TYPES = ["injection_overt", "injection_evasive",
                    "poisoning_overt",  "poisoning_evasive"]

    # Exp B
    print("\n" + "=" * 60 + "\nExp B — Per attack cell")
    test_mask = splits == "test"
    exp_b_trace = {}
    for atype in ATTACK_TYPES:
        mask = test_mask & (atypes == atype)
        if mask.sum() == 0:
            exp_b_trace[atype] = {"dr": None, "fpr": None, "n": 0}
            continue
        r = evaluate(clf, X[mask], y[mask])
        exp_b_trace[atype] = {"dr": r["dr"], "fpr": r["fpr"], "n": int(mask.sum())}
        print(f"  {atype:<25}  DR={r['dr']:.1%}  n={mask.sum()}")

    print("\nStatic scanner:")
    static_r = exp_static(trajs, splits, y)

    # Exp C
    print("\n" + "=" * 60 + "\nExp C — Security-utility frontier")
    c = exp_c(clf, X_te, y_te)

    # Exp D
    print("\n" + "=" * 60 + "\nExp D — Feature ablation")
    d = exp_d(clf, X_tr, y_tr, X_te, y_te, base_auc)

    # Exp F
    print("\n" + "=" * 60 + "\nExp F — Behavioral rule baseline")
    f = exp_f(trajs, splits, y)

    # Exp G
    print("\n" + "=" * 60 + "\nExp G — Adaptive attacker (partial suppression)")
    g = exp_g(clf, X, y, splits)

    # Exp G2
    print("\n" + "=" * 60 + "\nExp G2 — Adaptive attacker (F1+F2+F3 suppressed)")
    g2 = exp_g2(clf, X, y, splits)

    # Exp M2
    print("\n" + "=" * 60 + "\nExp M2 — LR on F1 features only")
    m2 = exp_m2(X, y, splits)

    # Exp M3 (LOTO)
    print("\n" + "=" * 60 + "\nExp M3 — Leave-one-template-out CV")
    m3 = exp_m3(trajs, X, y)

    # Exp S
    print("\n" + "=" * 60 + "\nExp S — Step-level detection")
    test_trajs = [trajs[i] for i in range(len(trajs)) if splits[i] == "test"]
    s = exp_s(test_trajs, y_te, clf)

    # Exp L
    print("\n" + "=" * 60 + "\nExp L — Inference latency")
    l = exp_l(clf, X_te)

    # LR all features
    print("\n" + "=" * 60 + "\nLR (all 30 features) baseline")
    lr_all = exp_lr_all(X, y, splits)

    # Random Forest
    print("\n" + "=" * 60 + "\nRandom Forest (200 trees) baseline")
    rf = exp_rf(X, y, splits)

    # ── Save all ──────────────────────────────────────────────────────────────
    results_path = Path("results/experiments.json")
    results = json.loads(results_path.read_text()) if results_path.exists() else {}

    results.update({
        "n_trajectories": len(trajs),
        "n_attack":       int((y == 1).sum()),
        "n_benign":       int((y == 0).sum()),
        "feature_dim":    int(X.shape[1]),
        "exp_a": {
            "val":  {k: v for k, v in val_r.items()  if k not in ("scores", "y_true")},
            "test": {k: v for k, v in test_r.items() if k not in ("scores", "y_true")},
        },
        "exp_b": {
            "trace":          exp_b_trace,
            "static_scanner": static_r,
        },
        "exp_c": c,
        "exp_d": d,
        "exp_f": f,
        "exp_g": g,
        "exp_g2": g2,
        "exp_m2": m2,
        "exp_m3": m3,
        "exp_s":  s,
        "exp_l":  l,
        "exp_lr_all": lr_all,
        "exp_rf":     rf,
    })

    results_path.write_text(json.dumps(results, indent=2))
    print(f"\n{'='*60}")
    print(f"All results saved → {results_path}")
    print(f"Dataset: {len(trajs)} trajectories — all experiments consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

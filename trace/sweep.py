"""Security-utility frontier sweep (Algorithm 2 from the paper)."""
from typing import List, Dict
import numpy as np


def frontier(
    attack_scores: np.ndarray,
    benign_scores: np.ndarray,
    step: float = 0.01,
) -> List[Dict]:
    """
    Sweep threshold from 0→1 and record (utility, security) pairs.

    security(θ) = fraction of attack runs blocked  (score > θ)
    utility(θ)  = fraction of benign runs NOT blocked (score ≤ θ)
    """
    points = []
    for theta in np.arange(0.0, 1.0 + step, step):
        sec  = float((attack_scores > theta).mean())
        util = float((benign_scores <= theta).mean())
        points.append(
            {"theta": round(float(theta), 3), "security": sec, "utility": util}
        )
    return points


def operating_points(
    pts: List[Dict],
    utility_floors: List[float] = (0.95, 0.90, 0.85, 0.80, 0.70),
) -> Dict:
    """For each utility floor, find the best (highest security) achievable point."""
    result = {}
    for floor in utility_floors:
        candidates = [p for p in pts if p["utility"] >= floor]
        if candidates:
            best = max(candidates, key=lambda p: p["security"])
            result[floor] = best
        else:
            result[floor] = None
    return result

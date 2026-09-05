"""F1-F5 feature extraction for TRACE."""
import re
import base64
from collections import Counter
from urllib.parse import urlparse
from typing import List, Dict, Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------------------------
# Global TF-IDF vectorizer (fit once on all task descriptions + action texts)
# ---------------------------------------------------------------------------
_tfidf = TfidfVectorizer(max_features=300, min_df=1)
_tfidf_fitted = False


def fit_tfidf(texts: List[str]) -> None:
    global _tfidf_fitted
    _tfidf.fit(texts)
    _tfidf_fitted = True


# ---------------------------------------------------------------------------
# F1: Tool call sequence bigrams
# ---------------------------------------------------------------------------
BIGRAM_VOCAB = [
    "read_file__fetch_url",
    "read_file__shell_exec",
    "shell_exec__fetch_url",
    "fetch_url__fetch_url",
    "load_skill__fetch_url",
    "fetch_url__shell_exec",
    "shell_exec__shell_exec",
    "write_file__fetch_url",
    "read_file__write_file",
    "fetch_url__write_file",
]

UNIGRAM_VOCAB = [
    "fetch_url", "read_file", "write_file", "shell_exec", "load_skill"
]


def f1_sequence_ngrams(steps: List[Dict]) -> np.ndarray:
    tools = [s["tool"] for s in steps]
    bigrams = [f"{a}__{b}" for a, b in zip(tools[:-1], tools[1:])]
    counts = Counter(bigrams + tools)
    vec = np.array(
        [counts.get(v, 0) for v in BIGRAM_VOCAB + UNIGRAM_VOCAB],
        dtype=float,
    )
    return vec


# ---------------------------------------------------------------------------
# F2: Argument anomalies
# ---------------------------------------------------------------------------
def _looks_base64(s: str) -> bool:
    s = s.strip()
    if len(s) < 16:
        return False
    if not re.match(r'^[A-Za-z0-9+/]+=*$', s):
        return False
    try:
        decoded = base64.b64decode(s + "==")
        return len(decoded) > 8
    except Exception:
        return False


def f2_arg_anomalies(steps: List[Dict]) -> np.ndarray:
    n_base64 = 0
    external_hosts: set = set()
    deep_paths = 0
    long_args = 0
    post_calls = 0

    for step in steps:
        args = step.get("args", {})
        for key, val in args.items():
            val_str = str(val)
            if _looks_base64(val_str):
                n_base64 += 1
            if len(val_str) > 300:
                long_args += 1
            if key == "url":
                parsed = urlparse(val_str)
                if parsed.netloc:
                    external_hosts.add(parsed.netloc)
            if key == "path" and val_str.count("/") > 3:
                deep_paths += 1
        if step.get("tool") == "fetch_url":
            method = args.get("method", "GET").upper()
            if method == "POST":
                post_calls += 1

    return np.array(
        [n_base64, len(external_hosts), deep_paths, long_args, post_calls],
        dtype=float,
    )


# ---------------------------------------------------------------------------
# F3: Network destination consistency
# ---------------------------------------------------------------------------
def _extract_implied_hosts(task: str) -> set:
    pattern = r'(?:https?://)?([a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z]{2,})+)'
    matches = re.findall(pattern, task)
    return {m.lower() for m in matches}


def f3_network_consistency(steps: List[Dict], task: str) -> np.ndarray:
    implied = _extract_implied_hosts(task)
    actual_hosts: set = set()
    for step in steps:
        url = step.get("args", {}).get("url", "")
        if url:
            host = urlparse(url).netloc.lower()
            if host:
                actual_hosts.add(host)

    if not actual_hosts:
        return np.array([0.0, 0.0], dtype=float)

    out_of_policy = actual_hosts - implied
    frac_oop = len(out_of_policy) / len(actual_hosts)
    return np.array([frac_oop, len(actual_hosts)], dtype=float)


# ---------------------------------------------------------------------------
# F4: Intent-action consistency (TF-IDF cosine distance)
# ---------------------------------------------------------------------------
def f4_intent_consistency(steps: List[Dict], task: str) -> np.ndarray:
    if not steps:
        return np.array([0.0], dtype=float)

    action_parts = []
    for s in steps:
        parts = [s["tool"]] + [str(v) for v in s.get("args", {}).values()]
        action_parts.append(" ".join(parts))
    action_text = " ".join(action_parts)

    if not _tfidf_fitted or not action_text.strip():
        return np.array([0.5], dtype=float)

    try:
        vecs = _tfidf.transform([task, action_text])
        sim = cosine_similarity(vecs[0], vecs[1])[0, 0]
        return np.array([1.0 - float(sim)], dtype=float)
    except Exception:
        return np.array([0.5], dtype=float)


# ---------------------------------------------------------------------------
# F5: Structural anomalies
# ---------------------------------------------------------------------------
PRIV_TOOLS = {"shell_exec", "load_skill"}
WRITE_TOOLS = {"write_file"}
READ_TOOLS = {"read_file", "fetch_url"}


def f5_structural(steps: List[Dict]) -> np.ndarray:
    n = len(steps)
    if n == 0:
        return np.zeros(7, dtype=float)

    tools = [s["tool"] for s in steps]
    n_unique = len(set(tools))

    # Max consecutive run of the same tool
    max_run = cur_run = 1
    for i in range(1, len(tools)):
        cur_run = cur_run + 1 if tools[i] == tools[i - 1] else 1
        max_run = max(max_run, cur_run)

    n_priv = sum(1 for t in tools if t in PRIV_TOOLS)
    n_writes = sum(1 for t in tools if t in WRITE_TOOLS)
    n_reads = sum(1 for t in tools if t in READ_TOOLS)
    n_errors = sum(1 for s in steps if not s.get("result_ok", True))

    return np.array(
        [n, n_unique, max_run, n_priv, n_writes, n_reads, n_errors],
        dtype=float,
    )


# ---------------------------------------------------------------------------
# Combined feature extraction
# ---------------------------------------------------------------------------
def extract_features(trajectory: Dict[str, Any]) -> np.ndarray:
    steps = trajectory.get("steps", [])
    task = trajectory.get("task_description", "")
    return np.concatenate([
        f1_sequence_ngrams(steps),   # 15 dims
        f2_arg_anomalies(steps),     #  5 dims
        f3_network_consistency(steps, task),  # 2 dims
        f4_intent_consistency(steps, task),   # 1 dim
        f5_structural(steps),                 # 7 dims
    ])  # total: 30 dims

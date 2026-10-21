"""Reads REAL evaluation results from the evaluation/ folder (if present).

Nothing here invents numbers: if the files are missing, the functions return None.
Create the files by running:  python scripts/evaluate_model.py --help
"""
from __future__ import annotations

import csv
import json

import numpy as np

from . import config

CM_FILE = config.EVAL_DIR / "confusion_matrix.csv"
REPORT_FILE = config.EVAL_DIR / "classification_report.txt"
METRICS_FILE = config.EVAL_DIR / "metrics.json"


def load_confusion_matrix():
    """Return a 5x5 integer array (rows = true grade, columns = predicted grade) or None."""
    if not CM_FILE.is_file():
        return None
    rows = []
    with open(CM_FILE, newline="") as fh:
        for row in csv.reader(fh):
            if row:
                rows.append([float(v) for v in row])
    cm = np.array(rows)
    if cm.shape != (config.NUM_CLASSES, config.NUM_CLASSES) or (cm < 0).any():
        raise ValueError(f"{CM_FILE.name} must be a 5 x 5 table of non-negative counts.")
    return cm.astype(int)


def metrics_from_confusion(cm: np.ndarray) -> dict:
    """Per-class precision / recall / F1 / support and accuracy, computed from the matrix."""
    tp = np.diag(cm).astype(float)
    support = cm.sum(axis=1).astype(float)
    predicted = cm.sum(axis=0).astype(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        precision = np.where(predicted > 0, tp / predicted, 0.0)
        recall = np.where(support > 0, tp / support, 0.0)
        f1 = np.where(precision + recall > 0, 2 * precision * recall / (precision + recall), 0.0)
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "support": support.astype(int),
        "accuracy": float(tp.sum() / cm.sum()) if cm.sum() else 0.0,
        "macro_f1": float(f1.mean()),
    }


def load_report_text():
    return REPORT_FILE.read_text(encoding="utf-8") if REPORT_FILE.is_file() else None


def load_metrics_json():
    if not METRICS_FILE.is_file():
        return None
    return json.loads(METRICS_FILE.read_text(encoding="utf-8"))

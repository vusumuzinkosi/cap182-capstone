"""
evaluate.py – metric tools shared between CAP182 SS2 models (and compare_models.py).

Accuracy is not a good metric in our case because the positive target is
imbalanced (11% positive samples). Precision, recall, F1-score, ROC AUC and
PR AUC (average precision) metrics are provided to show a balance in
business (find the customers without sending too many false positives to
the team) – same logic as in the problem description for SS1.
"""
from __future__ import annotations
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    balanced_accuracy_score,
)


def compute_metrics(y_true, y_pred, y_proba) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    specificity = tn / (tn + fp) if (tn + fp) else 0.0
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "specificity": specificity,
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_proba),
        "pr_auc": average_precision_score(y_true, y_proba),
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
    }


def metrics_table(metrics: dict) -> str:
    """Render a metrics dict as a Markdown table row block."""
    order = ["accuracy", "balanced_accuracy", "precision", "recall",
             "specificity", "f1", "roc_auc", "pr_auc"]
    lines = ["| Metric | Value |", "|---|---|"]
    for k in order:
        lines.append(f"| {k} | {metrics[k]:.4f} |")
    lines.append(f"| confusion (tn, fp, fn, tp) | {metrics['tn']}, {metrics['fp']}, "
                 f"{metrics['fn']}, {metrics['tp']} |")
    return "\n".join(lines)


def print_metrics(name: str, metrics: dict) -> None:
    print(f"\n=== {name} ===")
    for k in ["accuracy", "balanced_accuracy", "precision", "recall",
              "specificity", "f1", "roc_auc", "pr_auc"]:
        print(f"  {k:10s}: {metrics[k]:.4f}")
    print(f"  confusion (tn,fp,fn,tp): {metrics['tn']}, {metrics['fp']}, "
          f"{metrics['fn']}, {metrics['tp']}")

"""
SS3 Part D - follow-up checks requested by the client in Discussion #2.

Reuses the pipeline defined in SS3_PartB.ipynb as the single source of truth: the
relevant code cells are extracted from the notebook and executed, so these checks
cannot drift away from the submitted analysis.

Run from the repository root:

    python scripts/ss3_partd_checks.py

Writes:
    experimental-results/ss3_partd_seed_variation.json
    experimental-results/ss3_partd_cutoff_sweep.json
    experimental-results/ss3_partd_target_definition.json
"""
import contextlib
import io
import json
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (average_precision_score, confusion_matrix,
                             precision_recall_curve, roc_auc_score)

warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "experimental-results"
NOTEBOOK = REPO / "SS3_PartB.ipynb"

# Cells carrying configuration, loading, cohort selection, feature building,
# the time-based split and the fit. Figures and write-ups are not needed here.
_MARKERS = ("import os, json", "REPO_DIR", "_CANDIDATES", "def load_client_tables",
            "Integrity checks", "Target and modelling cohort", "Dataset summary",
            "build_analysis_frame", "Time-based train", "from sklearn.pipeline",
            "Fit on the training subset")


def _pipeline_source() -> str:
    nb = json.loads(NOTEBOOK.read_text())
    cells = [''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code']
    src = '\n\n'.join(s for s in cells if any(m in s for m in _MARKERS))
    src = src.replace("REPO_DIR    = Path.cwd()", "REPO_DIR    = Path(r'%s')" % REPO)
    src = re.sub(r"^import matplotlib.*$", "", src, flags=re.M)
    src = re.sub(r'^print\("matplotlib.*$', "", src, flags=re.M)
    return src


_SRC = _pipeline_source()


def run(cutoff_hours: int = 24, seed: int = 42) -> dict:
    """Execute the notebook pipeline with one cut-off and one seed."""
    src = _SRC.replace("FEATURE_CUTOFF_HOURS   = 24",
                       "FEATURE_CUTOFF_HOURS   = %d" % cutoff_hours)
    src = src.replace("RANDOM_STATE = 42", "RANDOM_STATE = %d" % seed)
    ns = {'__name__': '__main__'}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, 'ss3_pipeline', 'exec'), ns)
    return ns


def stall_lift(y_true, y_proba, k_frac: float = 0.20) -> float:
    """Lift for stalling among the k_frac lowest-scoring accounts (the SS1 metric)."""
    y_true = np.asarray(y_true)
    stalled = 1 - y_true
    k = max(int(len(y_true) * k_frac), 1)
    order = np.argsort(np.asarray(y_proba))[:k]
    base = float(stalled.mean())
    return (int(stalled[order].sum()) / k) / base if base else float('nan')


def evaluate(ns: dict) -> dict:
    """Threshold on validation, then score the untouched test block."""
    model = ns['model']
    pv = model.predict_proba(ns['X_valid'])[:, 1]
    prec, rec, thr = precision_recall_curve(ns['y_valid'], pv)
    f1 = 2 * prec * rec / np.clip(prec + rec, 1e-12, None)
    threshold = float(thr[int(np.nanargmax(f1[:-1]))])

    y_test = ns['y_test']
    pt = model.predict_proba(ns['X_test'])[:, 1]
    tn, fp, fn, tp = confusion_matrix(y_test, (pt >= threshold).astype(int),
                                      labels=[0, 1]).ravel()
    return dict(best_iteration=int(ns['BEST_ITERATION']), threshold=threshold,
                roc_auc=float(roc_auc_score(y_test, pt)),
                pr_auc=float(average_precision_score(y_test, pt)),
                precision=float(tp / (tp + fp)) if tp + fp else float('nan'),
                recall=float(tp / (tp + fn)) if tp + fn else float('nan'),
                specificity=float(tn / (tn + fp)) if tn + fp else float('nan'),
                lift_at_20pct=float(stall_lift(y_test, pt, 0.20)))


# --------------------------------------------------------------------------
# Question 1. Does the stricter Reversed flag definition change the target?
# --------------------------------------------------------------------------
def target_definition(ns: dict) -> dict:
    acc, dep = ns['tables']['accounts'].copy(), ns['tables']['deposits'].copy()
    for c in ('Registration time', 'Activation deadline'):
        acc[c] = pd.to_datetime(acc[c], format='ISO8601', errors='coerce')
    dep['Settled time'] = pd.to_datetime(dep['Settled time'], format='ISO8601',
                                         errors='coerce')
    flagged = set(acc.loc[acc['Activated 30d'].astype(str).str.lower()
                          .isin(['true', '1', 'yes']), 'Account ID'])

    d = dep.merge(acc[['Account ID', 'Registration time', 'Activation deadline']],
                  on='Account ID', how='left')
    settled_in_window = (
        (d['Deposit status'].str.lower() == 'settled')
        & (pd.to_numeric(d['Amount cents'], errors='coerce') > 0)
        & d['Settled time'].notna()
        & (d['Settled time'] <= d['Activation deadline'])
    )
    reversed_flag = d['Reversed flag'].astype(str).str.lower() == 'true'

    as_submitted = set(d.loc[settled_in_window, 'Account ID'])
    stricter = set(d.loc[settled_in_window & ~reversed_flag, 'Account ID'])

    late = d[d['Account ID'].isin(flagged - as_submitted)
             & (d['Deposit status'].str.lower() == 'settled')]
    hours_late = ((late['Settled time'] - late['Activation deadline'])
                  .dt.total_seconds() / 3600).dropna()

    return {
        "flagged_activated_30d": len(flagged),
        "rebuilt_settled_in_window": len(as_submitted),
        "flagged_but_not_rebuilt": len(flagged - as_submitted),
        "rebuilt_but_not_flagged": len(as_submitted - flagged),
        "settled_after_deadline": {
            "accounts": int(hours_late.shape[0]),
            "hours_late_min": round(float(hours_late.min()), 1),
            "hours_late_max": round(float(hours_late.max()), 1),
        },
        "reversal_fields": {
            "deposits_with_status_reversed": int((dep['Deposit status'].str.lower() == 'reversed').sum()),
            "deposits_with_reversed_flag_true": int((dep['Reversed flag'].astype(str).str.lower() == 'true').sum()),
            "settled_deposits_carrying_the_flag": int((
                (dep['Deposit status'].str.lower() == 'settled')
                & (dep['Reversed flag'].astype(str).str.lower() == 'true')).sum()),
        },
        "effect_of_stricter_definition": {
            "activated_as_submitted": len(as_submitted),
            "activated_excluding_reversed_flag": len(stricter),
            "accounts_changing_label": len(as_submitted - stricter),
        },
    }


# --------------------------------------------------------------------------
# Question 2. How much do the metrics move with the seed?
# --------------------------------------------------------------------------
SEEDS = [42, 1, 7, 13, 23, 99, 101, 202, 303, 404,
         505, 606, 707, 808, 909, 1234, 2024, 31337, 555, 777]


def seed_variation() -> dict:
    runs = {}
    for s in SEEDS:
        r = evaluate(run(24, s))
        r['seed'] = s
        runs[str(s)] = r
        print("  seed %-6s best_iteration %3d  roc_auc %.4f  lift %.3f"
              % (s, r['best_iteration'], r['roc_auc'], r['lift_at_20pct']), flush=True)
    keys = ('best_iteration', 'roc_auc', 'pr_auc', 'precision',
            'recall', 'specificity', 'lift_at_20pct')
    summary = {k: {"mean": float(np.mean([runs[str(s)][k] for s in SEEDS])),
                   "sd": float(np.std([runs[str(s)][k] for s in SEEDS], ddof=1)),
                   "min": float(np.min([runs[str(s)][k] for s in SEEDS])),
                   "max": float(np.max([runs[str(s)][k] for s in SEEDS]))}
               for k in keys}
    return {"n_seeds": len(SEEDS), "cutoff_hours": 24,
            "summary": summary, "runs": runs}


# --------------------------------------------------------------------------
# Question 3. What happens if the prediction point moves?
# --------------------------------------------------------------------------
CUTOFFS = (12, 24, 36, 48, 72)


def cutoff_sweep() -> dict:
    out = {}
    base = run(24, 42)
    acc = base['tables']['accounts'].copy()
    cohort = set(base['df']['Account ID'])
    acc = acc[acc['Account ID'].isin(cohort)]
    for c in ('Registration time', 'First deposit time'):
        acc[c] = pd.to_datetime(acc[c], format='ISO8601', errors='coerce')
    hours_to_fund = ((acc['First deposit time'] - acc['Registration time'])
                     .dt.total_seconds() / 3600)

    for h in CUTOFFS:
        r = evaluate(run(h, 42))
        r['cutoff_hours'] = h
        r['already_funded_by_cutoff'] = int((hours_to_fund <= h).sum())
        r['already_funded_pct'] = round(100 * r['already_funded_by_cutoff'] / len(acc), 2)
        r['intervention_window_days_left'] = round(30 - h / 24, 2)
        out[str(h)] = r
        print("  cut-off %2dh  best_iteration %3d  roc_auc %.4f  pr_auc %.4f  "
              "lift %.3f  already funded %d"
              % (h, r['best_iteration'], r['roc_auc'], r['pr_auc'],
                 r['lift_at_20pct'], r['already_funded_by_cutoff']), flush=True)
    return {"cohort_size": len(acc), "seed": 42, "runs": out}


if __name__ == '__main__':
    RESULTS.mkdir(parents=True, exist_ok=True)
    print("Question 1: target definition and the Reversed flag")
    q1 = target_definition(run(24, 42))
    print(json.dumps(q1, indent=2))
    (RESULTS / "ss3_partd_target_definition.json").write_text(json.dumps(q1, indent=2))

    print("\nQuestion 2: seed variation over %d seeds" % len(SEEDS))
    q2 = seed_variation()
    (RESULTS / "ss3_partd_seed_variation.json").write_text(json.dumps(q2, indent=2))

    print("\nQuestion 3: moving the prediction point")
    q3 = cutoff_sweep()
    (RESULTS / "ss3_partd_cutoff_sweep.json").write_text(json.dumps(q3, indent=2))

    print("\nWritten to experimental-results/ss3_partd_*.json")

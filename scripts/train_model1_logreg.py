"""
train_model1_logreg.py -- Model 1: Logistic Regression (CAP182 SS2).

Intelligible linear baseline. End-to-end pipeline:
    feature_engineering -> preprocessing -> LogisticRegression

class_weight='balanced' accounts for the ~11% positive class rate to prevent
the classifier from degenerating to the majority 'no' class prediction.

Output files (experimental-results/):
    model1_metrics.json     -- key performance metrics on the test set
    model1_predictions.csv  -- y_true, y_proba, y_pred (required by comparison)
Model object (models/):
    model1_logreg.joblib

Execute:  python scripts/train
"""
from __future__ import annotations
import os, json
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

from common import get_train_test, RESULTS_DIR, MODELS_DIR, RANDOM_STATE
from feature_engineering import make_feature_engineer
from preprocessing import build_preprocessor
from evaluate import compute_metrics, print_metrics

MODEL_NAME = "Model 1 - Logistic Regression"
PROBA_THRESHOLD = 0.5


def build_model() -> Pipeline:
    return Pipeline([
        ("features", make_feature_engineer()),
        ("preprocess", build_preprocessor()),
        ("clf", LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            solver="lbfgs",
            random_state=RANDOM_STATE,
        )),
    ])


def main() -> int:
    X_train, X_test, y_train, y_test = get_train_test()
    model = build_model()
    model.fit(X_train, y_train)

    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= PROBA_THRESHOLD).astype(int)
    metrics = compute_metrics(y_test, y_pred, y_proba)
    print_metrics(MODEL_NAME, metrics)

    joblib.dump(model, os.path.join(MODELS_DIR, "model1_logreg.joblib"))
    with open(os.path.join(RESULTS_DIR, "model1_metrics.json"), "w") as f:
        json.dump({"model": MODEL_NAME, **metrics}, f, indent=2)
    pd.DataFrame({"y_true": y_test.values, "y_proba": y_proba, "y_pred": y_pred}) \
        .to_csv(os.path.join(RESULTS_DIR, "model1_predictions.csv"), index=False)
    print("Saved model1 artefacts to models/ and experimental-results/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

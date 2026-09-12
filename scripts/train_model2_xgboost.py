"""
train_model2_xgboost.py -- Model 2: Gradient Boosting (XGBoost) (CAP182 SS2).

Non-linear gradient-boosted tree ensemble. Full pipeline:
    feature_engineering -> preprocessing -> XGBClassifier

scale_pos_weight = (#negatives / #positives) handles the class imbalance.
Hyper-parameters are set explicitly (see below) so the run is reproducible and
the choices can be described in Model2.MD.

Outputs (experimental-results/):
    model2_metrics.json
    model2_predictions.csv
Model artefact (models/):
    model2_xgboost.joblib

Run:  python scripts/train_model2_xgboost.py
Maps to: Model2.MD  and  Model2Performance.MD
"""
from __future__ import annotations
import os, json
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from common import get_train_test, RESULTS_DIR, MODELS_DIR, RANDOM_STATE
from feature_engineering import make_feature_engineer
from preprocessing import build_preprocessor
from evaluate import compute_metrics, print_metrics

MODEL_NAME = "Model 2 - XGBoost"
PROBA_THRESHOLD = 0.5

# Explicit hyper-parameters (describe these in Model2.MD).
HYPERPARAMS = dict(
    n_estimators=400,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_lambda=1.0,
    min_child_weight=1,
    objective="binary:logistic",
    eval_metric="logloss",
    tree_method="hist",
    random_state=RANDOM_STATE,
    n_jobs=-1,
)


def build_model(scale_pos_weight: float) -> Pipeline:
    return Pipeline([
        ("features", make_feature_engineer()),
        ("preprocess", build_preprocessor()),
        ("clf", XGBClassifier(scale_pos_weight=scale_pos_weight, **HYPERPARAMS)),
    ])


def main() -> int:
    X_train, X_test, y_train, y_test = get_train_test()
    pos = int(y_train.sum()); neg = int((y_train == 0).sum())
    spw = neg / max(pos, 1)
    print(f"Train balance: {pos} positive / {neg} negative -> scale_pos_weight={spw:.2f}")

    model = build_model(spw)
    model.fit(X_train, y_train)

    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= PROBA_THRESHOLD).astype(int)
    metrics = compute_metrics(y_test, y_pred, y_proba)
    print_metrics(MODEL_NAME, metrics)

    joblib.dump(model, os.path.join(MODELS_DIR, "model2_xgboost.joblib"))
    with open(os.path.join(RESULTS_DIR, "model2_metrics.json"), "w") as f:
        json.dump({"model": MODEL_NAME, **metrics}, f, indent=2)
    pd.DataFrame({"y_true": y_test.values, "y_proba": y_proba, "y_pred": y_pred}) \
        .to_csv(os.path.join(RESULTS_DIR, "model2_predictions.csv"), index=False)
    print("Saved model2 artefacts to models/ and experimental-results/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

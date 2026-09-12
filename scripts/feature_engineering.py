"""
feature_engineering.py -- domain features for CAP182 SS2.

Provides make_feature_engineer(), a FunctionTransformer from scikit-learn that
augments the Bank Marketing data frame with a handful of interpretable features.
It is the FIRST step of every model pipeline (after preprocessing) so that the
same transformations can be applied without fitting to both training and testing.

Feature Engineering
  - was_prev_contacted : True if the customer was contacted previously (pdays
                        does not equal 999), False otherwise. The UCI
                        sentinel for this is 999 which indicates not being
                        contacted before.
  - pdays              : The 999 sentinel is replaced by NaN such that the
                        value is imputed as an actual number rather than
                        messing up the scale.
  - has_prior_contacts : True if the previous variable is greater than 0.
  - age_group          : Life stage categorical buckets.
  - contact_intensity  : Categorized number of contacts in the current
                         campaign.

Mapped to: FeatureEngineering.MD
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.preprocessing import FunctionTransformer


def add_engineered_features(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy()

    if "pdays" in X.columns:
        X["was_prev_contacted"] = (X["pdays"] != 999).astype(int)
        X["pdays"] = X["pdays"].replace(999, np.nan)

    if "previous" in X.columns:
        X["has_prior_contacts"] = (X["previous"] > 0).astype(int)

    if "age" in X.columns:
        X["age_group"] = pd.cut(
            X["age"], bins=[0, 25, 35, 45, 55, 65, 200],
            labels=["<=25", "26-35", "36-45", "46-55", "56-65", "65+"],
        ).astype(object)

    if "campaign" in X.columns:
        X["contact_intensity"] = pd.cut(
            X["campaign"], bins=[0, 1, 3, np.inf],
            labels=["1", "2-3", "4+"],
        ).astype(object)

    return X


def make_feature_engineer() -> FunctionTransformer:
    """Return a stateless transformer that applies add_engineered_features."""
    return FunctionTransformer(add_engineered_features, validate=False)


if __name__ == "__main__":
    # Quick smoke test / preview of the engineered columns.
    from common import get_train_test
    X_train, X_test, y_train, y_test = get_train_test()
    out = add_engineered_features(X_train)
    new_cols = [c for c in out.columns if c not in X_train.columns]
    print("Rows:", len(out))
    print("Engineered columns added:", new_cols)
    print(out[new_cols].head())

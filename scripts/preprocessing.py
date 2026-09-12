"""
preprocessing.py -- preprocessing pipeline for CAP182 SS2.

Provides build_preprocessor(), a ColumnTransformer which does the following:
  - numeric features    -> median imputation + standardisation
  - categorical features -> most-frequent imputation + one-hot encoding
                            (handle_unknown='ignore' so that unseen categories 
                            during testing won't throw an error)

The columns are filtered based on their data type (make_column_selector), such 
that all columns created through feature engineering performed by 
feature_engineering.py are automatically included. Training occurs in each model's
Pipeline within the TRAINING split, thus avoiding any test-train leakage.

Note regarding 'duration': this is removed from common.get_train_test() prior to
this step because this feature is only known after the label and hence will 
leak the label (as per UCI docs; same discipline as in SS1).

Mapped to: Preprocessing.MD
"""
from __future__ import annotations
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer


def build_preprocessor() -> ColumnTransformer:
    numeric_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, make_column_selector(dtype_include="number")),
            ("cat", categorical_pipe, make_column_selector(dtype_include=["object", "category"])),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )


if __name__ == "__main__":
    # Smoke test: fit on train, report the resulting feature-matrix shape.
    from common import get_train_test
    from feature_engineering import make_feature_engineer
    X_train, X_test, y_train, y_test = get_train_test()
    fe = make_feature_engineer()
    pre = build_preprocessor()
    Xt = pre.fit_transform(fe.fit_transform(X_train))
    print("Train matrix after preprocessing:", Xt.shape)
    print("Positive rate (train): {:.3f}".format(y_train.mean()))

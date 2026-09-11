"""
common.py - utility functions for CAP182 SS2.

Place where all file paths are kept, the definition of target, list of features
and the reproducible train-test split that all scripts (data preparation,
feature engineering, modeling and comparisons) see the same data.
"""
from __future__ import annotations
import os
import pandas as pd
from sklearn.model_selection import train_test_split

# Paths
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPTS_DIR)
DATA_DIR = os.path.join(REPO_DIR, "datasets")
RESULTS_DIR = os.path.join(REPO_DIR, "experimental-results")
MODELS_DIR = os.path.join(REPO_DIR, "models")
SETUP_DIR = os.path.join(REPO_DIR, "experimental-setup")
RAW_CSV = os.path.join(DATA_DIR, "bank-additional-full.csv")

for _d in (DATA_DIR, RESULTS_DIR, MODELS_DIR, SETUP_DIR):
    os.makedirs(_d, exist_ok=True)

# Problem definition
TARGET = "y"                 # 'yes' / 'no' -> subscribed a term deposit
POSITIVE_LABEL = "yes"
RANDOM_STATE = 42
TEST_SIZE = 0.20

"""
'duration' is intentionally EXCLUDED. As mentioned in the UCI documentation, call
duration is something that will be known ONLY when the call has finished, which
will leak the result and has to be removed from the data for a valid model. 
This follows the pattern of handling leakage introduced in the SS1 problem
statement. Please refer to Preprocessing.MD.
"""
LEAKAGE_COLUMNS = ["duration"]


def load_raw(path: str = RAW_CSV) -> pd.DataFrame:
    """Load the semicolon-separated Bank Marketing CSV as a DataFrame."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found at {path}. Run: python scripts/download_data.py"
        )
    df = pd.read_csv(path, sep=";")
    return df


def make_binary_target(df: pd.DataFrame) -> pd.Series:
    """Map the 'y' column to a 1/0 integer label (1 = subscribed)."""
    return (df[TARGET].astype(str).str.strip().str.lower() == POSITIVE_LABEL).astype(int)


def get_train_test(df: pd.DataFrame | None = None):
    """Return X_train, X_test, y_train, y_test with a consistent stratified split.

    'duration' is stripped from this to avoid any subsequent misuse.
    This function is used by all model scripts to maintain consistency in the split.
    """
    if df is None:
        df = load_raw()
    y = make_binary_target(df)
    X = df.drop(columns=[TARGET] + [c for c in LEAKAGE_COLUMNS if c in df.columns])
    return train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )


def feature_types(X: pd.DataFrame):
    """Split columns into numeric and categorical name lists."""
    numeric = X.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]
    return numeric, categorical

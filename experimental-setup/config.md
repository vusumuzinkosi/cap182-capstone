# Experimental setup (CAP182 SS2)

All settings live in `scripts/common.py` so every script shares them.

| Setting | Value | Rationale |
|---|---|---|
| Target | `y` -> 1 if `yes` (subscribed), else 0 | Binary classification. |
| Excluded feature | `duration` | Leakage: Known only after the call/outcome (UCI docs; SS1 leakage rule). |
| Split | Stratified 80% train / 20% test | Maintains the 11% of positive labels in both splits. |
| Random seed | 42 | Deterministic, reproducible results. |
| Imbalance handling | LogReg `class_weight='balanced'`; XGBoost `scale_pos_weight = neg/pos` | Prevents collapsing of both algorithms to the majority class. |
| Decision threshold | 0.50 | Default procedure, threshold tuning suggested for the future (Part D). |
| Dataset version | UCI `bank-additional-full.csv`; SHA-256 `74adfc578bf77a7ff4bb1ba4a9f8709d9e3c6907342959c2c8416847e0afb4d8` | Ensures that the data used in the experiment is public and pinned down exactly. |
| Software environment | Python 3.12.13 with exact versions in `requirements.txt` | Ensures that the results presented are reproducible. |


Since both algorithms have been trained and tested using the same split,
the test is statistically sound and includes the application of the McNemar
paired test as well. The preprocessing and imbalance are fit in the
training split only, whereas the test split is used only for the final
paired evaluation.

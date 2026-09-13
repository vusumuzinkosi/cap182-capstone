# Model 2 Performance - XGBoost (CAP182 SS2 - Part C)

**Related scripts:** scripts/train_model2_xgboost.py and scripts/evaluate.py

## How to run

~~~bash
python scripts/train_model2_xgboost.py
~~~

The script fits Model 2 and evaluates it using precisely the same 8,238-row
holdout test set and threshold value of 0.50 applied to Model 1.

## Results

| Metric | Value |
|---|---:|
| Accuracy | 0.8496 |
| Balanced accuracy | 0.7614 |
| Precision | 0.3972 |
| Recall (sensitivity) | 0.6476 |
| Specificity | 0.8752 |
| F1 | 0.4924 |
| ROC-AUC | 0.8090 |
| PR-AUC (average precision) | 0.4868 |

Confusion matrix (tn, fp, fn, tp): **6,398, 912, 327, 601**

## Interpretation

XGBoost detects 601 out of 928 subscribers, achieving recall of 0.648.
That means, the Model 2 reaches about the same coverage as logistic regression
but has fewer false positives (912 vs 1,043). Consequently, precision increases
to 0.397 – almost 40% of detected customers are subscribers. This improvement
is beneficial for the capacity-limited sales team as it results in fewer wasted
contacts without substantially lowering the number of reached potential
subscribers.

Model 2 outperforms Model 1 in terms of balanced accuracy, specificity,
F1-score, ROC-AUC and PR-AUC as well. The latter measure equals 0.487 which
is almost 4.3 times bigger than the 0.113 base rate. This metric is particularly
important considering the skewed nature of the target variable. Although Model 2
misses 2 true positives compared to Model 1, it misses 131 false positives.
Therefore, whether it is more preferable depends on the cost of a missed activator
compared to a superfluous contact.

Such performance difference is understandable since boosted trees have a better
ability to detect interactions and nonlinear decision boundaries. However, it comes
at the expense of increased opacity of individual predictions. The generated feature
importance summary provides some level of explainability but production
implementation of the model needs additional work in this regard.

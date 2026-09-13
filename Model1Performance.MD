# Model 1 Performance - Logistic Regression (CAP182 SS2 - Part C)

**Related scripts:** scripts/train_model1_logreg.py and scripts/evaluate.py

## How to run

~~~bash
python scripts/train_model1_logreg.py
~~~

The code implements training of Model 1 and testing this model once using the 
fixed 8,238 cases test set at probability threshold of 0.50.

## Results

| Metric | Value |
|---|---:|
| Accuracy | 0.8339 |
| Balanced accuracy | 0.7536 |
| Precision | 0.3663 |
| Recall (sensitivity) | 0.6498 |
| Specificity | 0.8573 |
| F1 | 0.4685 |
| ROC-AUC | 0.8020 |
| PR-AUC (average precision) | 0.4591 |

Confusion matrix (tn, fp, fn, tp): **6,267, 1,043, 325, 603**

## Interpretation

Since only 928 out of 8,238 test cases (11.3%) are positive, the accuracy is not
the main performance measure as it will be too low. Instead, the balanced accuracy,
recall, precision, F1 and PR-AUC are the most meaningful measures for evaluating
this classifier.

For the conventional 0.50 threshold, Logistic Regression classifier finds 603 out of
928 subscribers, resulting in recall 0.650. It is a decent screening rate, but due
to 1,043 false positives, the precision is just 0.366, meaning that only 37 of every
100 customers predicted to take any actions are actual subscribers. The outreach
team would then spend time and effort contacting a lot of people who do not
subscribe at all, so it is not just an incorrect prediction but also an extra cost.

The PR-AUC of 0.459 is more than 4.1 times higher than the 0.113 positive base
rate, which means that the classifier has considerable ranking ability. The
ROC-AUC of 0.802 shows that class separation is also high, and balanced accuracy
of 0.754 proves that the model is performing reasonably well for both classes.
It is, thus, a valid baseline, yet its false positive rate may be reduced further.

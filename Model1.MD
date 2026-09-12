# Model 1 - Logistic Regression (CAP182 SS2 - Part B)

**Related scripts:** scripts/train_model1_logreg.py, scripts/evaluate.py and
scripts/explain_models.py

## How to run

~~~bash
python scripts/train_model1_logreg.py
python scripts/explain_models.py
~~~
The training script runs on the entire pipeline, does the inference on the test set,
prints the metrics and saves the predictions and fitted pipeline. The explanation script
is executed after training both models.

## Technique and role

The Logistic Regression algorithm represents the log odds of the positive outcome
as a linear combination of the features after encoding. Logistic regression is
used as an interpretable baseline method because it is quick to train and
understand and offers coefficients to interpret the fitted relationships
that contribute positively or negatively to the subscription probability.
Having a solid baseline method helps prevent a complicated method from being
suggested simply due to its complexity.

## Pipeline

feature engineering -> preprocessing -> LogisticRegression

The entire Pipeline from scikit-learn is fit only on the training data and then saved as
models/model1_logreg.joblib. As the transformations are included in the classifier,
the same transformations will be applied while making predictions.

## Hyperparameters

| Parameter | Value | Rationale |
|---|---|---|
| solver | lbfgs | L2 regularized binary logistic regression optimizer. |
| max_iter | 1000 | Ensures that there are enough iterations for convergence after applying one-hot encoding. |
| class_weight | balanced | Gives more importance to the minority class as per the ratio of the training distribution and not as per sampling. |
| penalty | L2 (default) | Reduces coefficients and variance if the encoded input is correlated. |
| C | 1.0 (default) | Used as an unoptimized base to evaluate Model 2. |
| random_state | 42 | Reproducibility. |
| decision threshold | 0.50 | Set a fixed operating point for a head-to-head evaluation. |

## Fitted associations


The most significant fitted positive coefficients involve the number of contacts
in March, consumer price index, cellular contacts, and previous contacts. The
negative coefficients are the employment variation rate, campaign months, telephone
contacts, and the number of contacts in campaigns. These are conditional
relationships rather than causative factors; the use of one-hot encoding and
correlated macroeconomic variables means that individual coefficients should
be interpreted carefully.

The complete ranked output can be found in
experimental-results/feature_effects.md. It is used to validate the baseline,
and not to say that any single variable causes subscription.

## Outputs

| Output | Purpose |
|---|---|
| experimental-results/model1_metrics.json | Held-out evaluation metrics reproducibility and confusion matrix counts. |
| experimental-results/model1_predictions.csv | Row-wise true label and probability and predictions for comparison. |
| models/model1_logreg.joblib | Training to inference pipeline serialisation (excluded from Git as it is regenerateable). |


# Model 2 - XGBoost (CAP182 SS2 - Part B)

**Related scripts:** scripts/train_model2_xgboost.py, scripts/evaluate.py and
scripts/explain_models.py

## How to run

~~~bash
python scripts/train_model2_xgboost.py
python scripts/explain_models.py
~~~
The script for training is suitable for the whole pipeline, carries out inference 
on the same test rows used for Model 1, prints metrics and stores predictions as 
well as the fitted model.

## Technique and role

XGBoost is a gradient boosted tree method. This model creates shallow trees
one after another, and each subsequent tree tries to minimize errors created
by previous ensemble. In contrast to the linear benchmark, it is capable of
learning non-linear splits and interactions without specifying them explicitly.
This makes it a better candidate model.

## Pipeline

feature engineering -> preprocessing -> XGBClassifier

The trained model is saved to models/model2_xgboost.joblib, so training and prediction
utilize the same feature processing pipeline.

## Hyperparameters

| Parameter | Value | Rationale |
|---|---:|---|
| n_estimators | 400 | Sufficient number of boosting iterations, combined with a conservative learning rate. |
| learning_rate | 0.05 | Minor improvements lead to increased stability and lower chances of overfitting to individual trees. |
| max_depth | 5 | Allows capturing moderate interaction effects but controls tree complexity. |
| subsample | 0.8 | Row sampling per tree for regularisation. |
| colsample_bytree | 0.8 | Feature sampling per tree for regularisation. |
| reg_lambda | 1.0 | Regularises leaf weights using L2 penalty. |
| min_child_weight | 1 | Uses the traditional minimum child weight parameter. |
| scale_pos_weight | 7.88 | Has the negative-to-positive ratio of the training fold (29,238 / 3,712). |
| tree_method | hist | Efficient histogram-based tree building. |
| objective / metric | binary:logistic / logloss | Generates probabilities for binary classification problems. |
| random_state | 42 | Reproducibility. |
| decision threshold | 0.50 | Common default parameters setting for the presented comparison. |


The following parameters have been selected prior to testing on the final hold-out sample. 
It is advisable to do a cross-validation search prior to deployment, but without influencing 
the test dataset.

## Fitted importance summary

The top XGBoost importance scores are nr.employed, October contact, 
was_prev_contacted, emp.var.rate, cons.conf.idx, and prior campaign success.
Importance has no directionality - it implies that the tree model used this
feature to decrease the loss function, rather than increasing the score
or generating the target value. The complete ranked list can be found in 
experimental-results/feature_effects.md.

## Outputs

| Output | Purpose |
|---|---|
| experimental-results/model2_metrics.json | Reproducibility metrics using held-out data and confusion matrices. |
| experimental-results/model2_predictions.csv | True labels and predictions row aligned for easy comparison. |
| models/model2_xgboost.joblib | Serialisation of the training to inference pipeline (not in Git because it is regeneratable). |


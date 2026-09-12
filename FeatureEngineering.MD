# Feature Engineering (CAP182 SS2 - Part B)

**Related script:** scripts/feature_engineering.py

## How to run

~~~bash
python scripts/feature_engineering.py
~~~



The code shows the engineered features for the fixed training set. For both models,
feature engineering is done at the first stage and is performed the same way during
training and prediction.

## Engineered features

| Transformation | Definition | Modelling rationale | STADIOEquities analogue |
|---|---|---|---|
| was_prev_contacted | 1 when pdays is not the 999 sentinel; otherwise 0 | Distinguishes between the presence of prior campaign interaction history and the time elapsed since that last interaction. | Whether the user had a prior meaningful interaction with the campaign, session or adviser. |
| pdays (cleaned) | Replace the 999 sentinel with a missing value | Ensures that the category representing "never contacted" does not function as a massive time-since-interaction value for the numeric imputer down the line. | Separate "no prior event" from real time since interaction values. |
| has_prior_contacts | 1 when previous is greater than zero | Indicates if there is any interaction history at all, using a simple, interpretable variable. | Whether the user interacted with the application or support team prior to the scoring date. |
| age_group | Bin age into <=25, 26-35, 36-45, 46-55, 56-65 and 65+ | Allows the linear model to approximate non-linear impacts of life stages without forcing a linear form. | General case of creating categorical bands for continuous customer characteristics where appropriate. |
| contact_intensity | Bin campaign contacts into 1, 2-3 and 4+ | Models the effect of diminishing returns and fatigue from continued interaction in campaigns. | Session or notification intensity bands prior to first funding. |

## Design and leakage control

These transformations are deterministic and stateless and do not derive
means, targets or category counts from the entire data set. These can therefore
be computed on top of the fitted preprocessor without exposing information
from the test data. The four additional columns are calculated within the
FunctionTransformer object which is then serialized along with the fitted model.

The feature space is deliberately kept small and interpretable. It provides
non-linear relationships for Logistic Regression while enabling XGBoost to
explore further interactions on its own. Overengineering features based on speculation
would complicate the explanation of the public proof-of-viability submission.

## Limitations and next step

The public data concerns the bank telemarketing process as opposed to the
activation of the app and therefore these features set modelling standards
as opposed to a definitive production standard. Once we have access to the
STADIOEquities data, the same approach should be followed for features
related to the completion of KYC, early activity of the app, source of
acquisition, support interactions, and time-based features up to the 24-hour
scoring cut-off point.


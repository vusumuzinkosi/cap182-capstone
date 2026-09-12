# Preprocessing (CAP182 SS2 - Part B)

**Related scripts:** scripts/common.py and scripts/preprocessing.py

## How to run

~~~bash
python scripts/preprocessing.py
~~~

The smoke test reads in the public dataset, performs the splitting to obtain the fixed training set, pre-processes the training dataset alone, and outputs the shape of the pre-processed matrix. Both models perform their preprocessing automatically.

## Data definition and split

The source dataset has 41,188 records, 20 predictor variables, and the target variable y.
The target variable is assigned 1 when the answer is yes (subscriber) and 0 otherwise.
A stratified train/test split 80/20 with the seed value 42 yields 32,950 records for training and 8,238 records for testing while keeping the positive rate of 11.3%. Both the models have the same number of records.

The duration variable is dropped before the split feeds into any downstream transformer.
Duration is determined once a marketing call has been completed; hence, the duration variable is unknown during scoring. Dropping this variable avoids target leakage and complies with the rule SS1 that allows using STADIOEquities model with information available up until the scoring cut-off point.

## Input columns after leakage control

| Type | Count | Columns |
|---|---:|---|
| Numeric | 9 | age, campaign, pdays, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed |
| Categorical | 10 | job, marital, education, default, housing, loan, contact, month, day_of_week, poutcome |

Feature engineering then includes two numeric indicators and two categorical ranges. The resulting preprocessed object generates 73 predictors based on the 23 engineered features.

## Processing pipeline

The build_preprocessor() method returns a scikit-learn ColumnTransformer which consists of the following branches:

| Branch | Steps | Purpose |
|---|---|---|
| Numeric | Median imputation, then StandardScaler | A reliable alternative for the missing value of cleaned pdays and ensures that numeric features are on equal scales. |
| Categorical | Most-frequent imputation, then one-hot encoding | Categories to indicator values, and safely ignores new categories found in inference. |

Columns are selected based on their types and therefore the newly created features are automatically pipelined without a predefined list of features. Feature standardization is important for the logistic regression model as its coefficient computation and regularization are scale dependent. It is not needed by tree splits but using the same preprocessor ensures a fair comparison between the two models.

## Leakage and reproducibility controls

The feature engineer, imputers, scaler and encoder are trained in each scikit-learn Pipeline only on the training fold. The test data is then transformed with these trained objects, ensuring that no information about the medians, frequency of categories or scaling from the test data leaks into the training fold. The random seed, test set size, label mapping and excluded columns are defined centrally in scripts/common.py.

The official CSV used for the verified run has SHA-256:

74adfc578bf77a7ff4bb1ba4a9f8709d9e3c6907342959c2c8416847e0afb4d8


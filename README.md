# CAP182 Capstone - STADIOEquities Account Activation

**Author:** Vusumuzi Nkosi  
**Student number:** 26303296  
**Module:** CAP182 Capstone Project, STADIO  
**Client:** STADIOEquities (retail investing and fintech)

In this repository, all the CAP182 capstone can be found as per its different stages of submission. The first submission (SS1) is the proposal for the project that contains motivation, problem definition, data request by the client and the log of RAAIDD. The second submission (SS2) is the proof of feasibility that tests the approach used in SS1 with a public data set before providing the client data.

---

# Submission 1 (SS1): Project proposal


## Motivation

### 1.1 Business context

The STADIOEquities platform used for retail investments depends on generating conversion between registrant and investor relationships that will generate value in the long run. Presently, the platform already has considerable scale – from the documentation provided by the clients, there are about 2.3 million accounts that have been registered, out of which, around 760,000 are funded accounts. This indicates that the area of opportunity is not just the increase in number of registrations, but in the funding of accounts by clients.

### 1.2 The business pain and its cost

There are financial and strategic considerations with respect to the activation gap. From the briefing pack, it was noted that 41% of the customers who have registered never go on to make a deposit, and the cost of acquisition of such a customer is R180 which is recovered through activation. This means that there is a loss of marketing resources where there is dormancy. Further deterioration is expected because there has been a decrease in conversion from registration to making deposits from 64% to 59%, while for six months' dormancy from 22% to 31%. This implies that there must be something wrong in the customer journey process but not necessarily in the interest of the customer. The same onboarding process may not be applied to all accounts because some might activate by themselves, while others may not continue due to some reasons.

### 1.3 Why this is the right problem now

This project has been designed keeping in mind the strategy of 2030 which states that “activate our existing accounts.” This project has been designed in compliance with the objectives set by the CEO who wants to develop “a lifetime of investing with customers” wherein the investment journey begins only after making the first deposit. Delay at this stage after registering is not permissible since interest would be lost then.

### 1.4 Value of a data-science solution

This scoring model takes into account information at the time of registration combined with the information within the first 24 hours, including the channel used, the status of the KYC, initial behavior within the application, goals set by the user, and the level of friction when seeking support, to identify the probability of success of each account at making its first deposit in the next 30 days. STADIOEquities will be able to allocate more resources, including human intervention, educational materials, prompts, and easy funding, for the high-risk accounts, while avoiding inundating the low-risk customers with too much interaction. The features analysis will help in identifying the common challenges faced by customers during the journey for the product and operations teams. The metrics used to evaluate the performance of the model are recall, precision, area under the precision-recall curve, and lift within the highest risk customers, but not accuracy, as the accuracy of the model is not important for the business.

### 1.5 Expected contribution

This exercise is a means of re-framing the costly activation gap as a quantifiable decision, specifically, who are the new customers that require additional assistance to be onboarded at this very moment. An increase in the deposit ratio, no matter how slight, will result in the saving of unnecessary acquisition expenses and will grow the pool of future investments.

## Problem statement

STADIOEquities has a lot of new registrations but at the same time a relatively big share of these accounts is not advancing to making the first deposit. The briefing pack refers to the declining sign-up to deposit conversion ratio and the growth of early dormancy. That makes customer acquisition expensive. Currently, there is no data-driven and repeatable method for selecting the accounts which can potentially self-activate and the accounts which are expected to stall.

The goal of the capstone project is solving the problem of prediction of success of making the first deposit within 30 calendar days from the registration date for every new account of STADIOEquities. Prediction should be made no later than 24 hours after registration and it should be made using the account and KYC features and customer's behavior within 24 hours after registration. Features available after the 24-hours cut-off date such as dates of the first deposits, balances and trading activity will be used to create or validate the outcome and will not be used as predictors.

The capstone will give the reproducible binary classification baseline, will compare different classifiers, will define the threshold value for the decision. The project will be successful when the model will outperform no-skill baseline on separated in time data and will provide an uplift among the accounts predicted to stall. The classifier is a tool for onboarding prioritisation and it does not make any decisions regarding access, KYC, pricing or investment eligibility.

## Data request (Part C)

The full client data specification for this project is provided as a PDF at [data-request/CAP182_SS1_Data_Request.pdf](data-request/CAP182_SS1_Data_Request.pdf).

## RAAIDD log

### Risks

| # | Specific risk for this project |
|---:|---|
| 1 | No successful first-deposit event or more than one or inconsistency in recording it makes it impossible to provide an accurate 30-day activation tag. |
| 2 | Information such as current balance, first deposit date, or other actions can give away the target variable in advance of model construction. |
| 3 | Account ID may be inconsistent among different databases, including account, applications, marketing, compliance, and support databases, reducing the training set size due to selection bias towards better-recorded customers. |
| 4 | Behavior and distribution of dormant/stalled accounts can shift following campaign or application release or new KYC procedure leading to performance drift. |
| 5 | Too many false positives from the onboarding team can lead to too much customer contact making the model essentially unusable. |
| 6 | Personal, behavioral, and compliance information can be used for activation purposes, unless certain management of identifiers and retention controls are put in place.  |

### Actions

| # | Action in the project lifecycle |
|---:|---|
| 1 | Agreement on operational activation, 24 hours feature cut off, 30 days outcomes window with the client. |
| 2 | Data Request submission and acquisition of de-identified extracts from eight data sources for client's data. |
| 3 | Key Profiling, date ranges definition, missing data and duplicates identification as well as referential integrity checks prior to source tables merging. |
| 4 | Activation flag recreation based on deposits events and reconciliation of the rate with the client's control totals. |
| 5 | Creation of only those features that are present in 24 hour score and explicit leakage assessment. |
| 6 | Transparent baseline creation, classification models training and their testing on a new time period. |
| 7 | Identification of the threshold based on onboarding capacity, recall, precision and lift and description of the trade-off between false negatives and false positives. |
| 8 | Subgroup performance analysis, privacy protection and operation feasibility discussion with the client prior to suggesting a pilot. |

### Assumptions

| # | Assumption currently believed but unproven |
|---:|---|
| 1 | An account which succeeds in depositing with a positive value in 30 days becomes a suitable and quantifiable measure of activation of the account. |
| 2 | At least 24 months’ data related to registrations and deposits exist and the latest period contains a whole 30-day observation window. |
| 3 | Using the same pseudonymized ID of an account will be sufficient to identify the needed data sources without relying on direct identifiers like names, ID numbers, e-mail addresses, or bank details. |
| 4 | The KYC status, digital footprint at sign-up, and acquisition context of 24 hours have additional insights than mere activation rate. |
| 5 | STADIOEquities has a legal ground for utilizing the above-mentioned data sources for the customer service use case in question. |
| 6 | The onboarding team can act upon the ranked risk list, and share its weekly reach capacity. |

### Issues

| # | Current issue |
|---:|---|
| 1 | Client datasets or data dictionary not provided, therefore availability of the fields, events semantics, cohort size, as well as the initial baseline 30-day activation rates can’t be verified at the moment.  |

### Decisions

| # | Decision made |
|---:|---|
| 1 | Client is known to be STADIOEquities, project scope is considered to be supervised binary prediction for first deposit activation and not the more general problem of dormancy. |
| 2 | Activation is considered to be successful positive-value deposit in 30 days and prediction is made based on data within 24 hours since registration. |
| 3 | Model allows for targeted customer onboarding only, it does not make automatic KYC verification, grant access to an account, sets pricing, marketing eligibility, or makes investments. |
| 4 | Evaluation will be performed based on the recall, precision, AUC of the precision-recall curve and top risk lift measures using time-based holdout evaluation approach. |

### Dependencies

| # | Dependency between project activities |
|---:|---|
| 1 | Label creation relies on definition of activation and completeness of registration, deposit, and timestamp fields. |
| 2 | Cross-source feature engineering relies on de-identification and joining of all the relevant tables using pseudonymized account ID. |
| 3 | Model training relies on data profiling, data cleansing, duplication reconciliation, and elimination of the fields that occur after the cut-off point of scoring. |
| 4 | Unbiased final evaluation will rely on definition and segregation of the later time-based test group before tuning of the model and thresholds. |
| 5 | Threshold setting will rely on validation of the probabilities and proof of the ability of contacting by the onboarding team as well as cost of the false positive/negatives. |
| 6 | Pilot run will rely on satisfactory offline model performance, sub-group analysis, privacy checks, stakeholder approval, and controlled score distribution to the onboarding team. |

---

# Submission 2 (SS2): Public-dataset proof of viability

A binary classification model for predicting whether a new STADIOEquities 
account will make their first deposit within 30 days was proposed by SS1. 
The second system (SS2) attempts to verify the effectiveness of the solution 
on a non-sensitive dataset, which is the Bank  Marketing Data Set from the UCI repository.

Two models are compared:

- **Model 1 - Logistic Regression:** an interpretable linear baseline.
- **Model 2 - XGBoost:** a non-linear gradient-boosted tree ensemble.

The duration field is deliberately excluded because it is known only after the
marketing call ends. This matches the SS1 rule that only information available
at scoring time may be used.

## Deliverables

| Part | Document | Related code |
|---|---|---|
| A | [Related Work and Data - PDF report](literature-review/CAP182_SS2_PartA_Related_Work.pdf) | Literature and dataset review (no code) |
| B | [Modelling - consolidated PDF report](reports/CAP182_SS2_PartB_Modelling.pdf) | Required separate Markdown documents listed below |
| B | [Preprocessing.MD](Preprocessing.MD) | scripts/preprocessing.py and scripts/common.py |
| B | [FeatureEngineering.MD](FeatureEngineering.MD) | scripts/feature_engineering.py |
| B | [Model1.MD](Model1.MD) | scripts/train_model1_logreg.py |
| B | [Model2.MD](Model2.MD) | scripts/train_model2_xgboost.py |
| C | [Results and Comparison - consolidated PDF report](reports/CAP182_SS2_PartC_Results.pdf) | Required separate Markdown documents listed below |
| C | [Model1Performance.MD](Model1Performance.MD) | scripts/train_model1_logreg.py and scripts/evaluate.py |
| C | [Model2Performance.MD](Model2Performance.MD) | scripts/train_model2_xgboost.py and scripts/evaluate.py |
| C | [Comparison.MD](Comparison.MD) | scripts/compare_models.py and scripts/explain_models.py |
| D | [Recommendations - PDF report](recommendations/CAP182_SS2_PartD_Recommendations.pdf) | Business recommendation report (no code) |

Parts A and D are provided as PDF reports. Parts B and C are provided as the separate Markdown files that the brief requires (linked above), each with an additional consolidated PDF report.

## Dataset

UCI Bank Marketing, bank-additional-full.csv:

- 41,188 rows
- 20 raw input columns plus the target y
- 4,640 positive cases (11.3%)
- 19 raw inputs after excluding duration
- SHA-256:
  74adfc578bf77a7ff4bb1ba4a9f8709d9e3c6907342959c2c8416847e0afb4d8

The raw CSV is ignored by Git and can be reproduced with
scripts/download_data.py.

## Verified held-out results

The fixed stratified split uses random seed 42 and an 80/20 train/test ratio.
Both models are evaluated on the same 8,238 test rows at threshold 0.50.

| Metric | Logistic Regression | XGBoost |
|---|---:|---:|
| Accuracy | 0.8339 | 0.8496 |
| Balanced accuracy | 0.7536 | 0.7614 |
| Precision | 0.3663 | 0.3972 |
| Recall | 0.6498 | 0.6476 |
| Specificity | 0.8573 | 0.8752 |
| F1 | 0.4685 | 0.4924 |
| ROC-AUC | 0.8020 | 0.8090 |
| PR-AUC | 0.4591 | 0.4868 |

XGBoost produces 131 fewer false positives while losing only two true positives.
McNemar's paired test gives p = 5.84 x 10^-8, supporting Model 2 as the stronger
model on this test set.

## Reproduce the experiment

The verified environment uses Python 3.12.13 and the exact package versions in
requirements.txt.

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_all.py
~~~

On macOS, XGBoost also needs the OpenMP runtime:

~~~bash
brew install libomp
~~~

Individual stages can be run with:

~~~bash
python scripts/download_data.py
python scripts/preprocessing.py
python scripts/feature_engineering.py
python scripts/train_model1_logreg.py
python scripts/train_model2_xgboost.py
python scripts/explain_models.py
python scripts/compare_models.py
~~~

## Reproducibility controls

- Random seed fixed and one stratified split used.
- Pre-processing done solely on training set.
- Duration measure, which is vulnerable to leakage, was not considered.
- Specific Python version numbers used were fixed.
- Checksum for dataset saved.
- Environment versions obtained via scripts/environment_report.py script.
- Models compared using paired holdout predictions.

---

# Submission 3 (SS3): The final method applied to the client data

SS2 implemented the approach with a publicly available proxy dataset. SS3 implements the same approach on the full STADIOEquities extract and describes its value to the onboarding team.

All parts of part B are implemented in a single notebook, [`SS3_PartB.ipynb`](SS3_PartB.ipynb), run from the root of the repository. The client data is not included in this write-up; the detailed description is available in [`datasets/client/README.md`](datasets/client/README.md), where the list of tables, the SHA-256 checksums, the target and window definitions, and the features excluded from modelling are provided.

## The data

Eight tables cover 1,841 registered accounts with the registration period from August 2024 to July 2026, in which all the outcome windows are mature. The row counts, keys, and referential integrity are consistent with the supplier's quality pack, and all the timestamps are ISO 8601.

**The modelling cohort consists of 1,133 accounts with `Registration status` equal to "complete"** (they activate with 62.6%). The remaining 708 accounts with the registration status of incomplete, rejected, cancelled, or closed activate with 0% – 2.2%; the outcomes of these users are pre-determined and considered the operational rule rather than a score input. The `Registration status` is excluded from predictors for the same reason, as it is an extract-time snapshot that encodes the outcome.

Features are derived only from the events that happened at or before the cut-off defined in SS1, which is registration plus 24 hours. Marketing events are the single exception to the lower bound, being filtered by the cut-off alone, because acquisition touchpoints happen earlier than registration.

## The method

XGBoost, the final method from SS2, continues to be used with the same pipeline. There were three hyperparameters adjusted for the cohort, which is roughly fifty times smaller than in SS2: `max_depth` decreased from 5 to 2, `min_child_weight` from 1 to 20, and `reg_lambda` from 1.0 to 10.0. The boosting was stopped once the validation log-loss had gone 50 consecutive rounds without improving. The justification of each adjustment is provided in the notebook. All other hyperparameters, including learning rate, sampling fractions, objective, and random seed, are the same as in SS2.

The data split is time-based rather than random: the earliest 60% of registrations make up the training subset, the next 20% make up the validation subset used for threshold determination, and the latest 20% form a hold-out test subset.

## Verified results for the unseen test subset

There were 227 accounts in the test subset, out of which 57.7% had a positive outcome. The threshold determined on the validation subset was set at 0.340.

| Metric | Training | Unseen test |
|---|---:|---:|
| ROC-AUC | 0.8215 | 0.7296 |
| PR-AUC | 0.8921 | 0.7682 |
| Precision | — | 0.6704 |
| Recall | — | 0.9160 |
| Specificity | — | 0.3854 |
| Confusion (tn, fp, fn, tp) | — | 37, 59, 11, 120 |

The boosting was stopped at iteration 318 out of 400 iterations ceiling. The difference in ROC-AUC between training and validation subsets is 0.088.

**Implications and value.** By ranking the registrations by stall risk and calling the bottom 20% of the new registrants, 75.6% of the contacted registrations stall. This gives a lift of 1.79x over random contacting and accounts for 35.4% of all the potential stallers. At 30% capacity, the number of stallers captured rises to 47.9%, while the lift reduces to 1.60x, meaning that this decision is about onboarding capacity but not about modelling performance.

**Comparative assessment with SS2, carried out with care.** While the headline precision and recall seem considerably better than SS2, the metrics are different depending on the base rate and represent 11.3% and 57.7% positive rates, respectively. As far as ROC-AUC, which is independent of the base rate, the client's model performs worse than the proof of concept (0.730 versus 0.809). The methodology is transferable and works well; however, this is a less challenging task with less room above chance than a more challenging one.

## SS3 deliverables

- Part A: Peer review report. Goes to Canvas, not held in this repository.
- Part B: Implementation of the final method on the client data. Location: [`SS3_PartB.ipynb`](SS3_PartB.ipynb); the results are archived in `experimental-results/ss3_*`
- Part C: Video presentation. Link will be put here after the recording.
- Part D: Answers to client questions. Available in this repository's Discussions tab.

## Reproduction of SS3

- Create and activate a virtual environment: `python3 -m venv .venv` then `source .venv/bin/activate`
- Install dependencies: `python -m pip install -r requirements.txt`
- Verify the client dataset: `shasum -a 256 datasets/client/*.csv`
- Run the notebook: `jupyter lab SS3_PartB.ipynb`, from the repository root, sequentially

---

## Repository structure

| Path | What it holds |
|---|---|
| `README.md` | This document: the SS1 proposal (motivation, problem statement, data request, RAAIDD) and the SS2 overview, results and links. |
| `data-request/` | SS1 Part C: the client data request PDF. |
| `Preprocessing.MD`, `FeatureEngineering.MD` | SS2 Part B: data preparation documents. |
| `Model1.MD`, `Model2.MD` | SS2 Part B: model implementation documents. |
| `Model1Performance.MD`, `Model2Performance.MD`, `Comparison.MD` | SS2 Part C: results and model comparison documents. |
| `literature-review/` | SS2 Part A: related-work review (PDF report). |
| `reports/` | SS2 consolidated Part B and Part C review reports (PDF). |
| `recommendations/` | SS2 Part D: recommendation report (PDF report). |
| `scripts/` | SS2 pipeline: data acquisition, preprocessing, feature engineering, training, evaluation, explanation and comparison. |
| `experimental-setup/` | Fixed experimental configuration and train/test split rules. |
| `experimental-results/` | SS2 metrics, paired predictions, comparison summary, feature effects and the ROC / precision-recall plot, plus the SS3 `ss3_*` metrics, predictions and figures. |
| `SS3_PartB.ipynb` | SS3 Part B: the full client-data notebook, loading through results visualisation. |
| `datasets/` | Local data location; the raw CSV is Git-ignored and downloaded via `scripts/download_data.py`. |
| `datasets/client/` | SS3 client extract. The data is Git-ignored; `datasets/client/README.md` documents it and records the checksums. |
| `models/` | Regenerable trained models; binaries are Git-ignored. |

## Evidence base

The current proposal uses the business statistics and data sources described in the STADIOEquities Information Pack for CAP182 SS1. The format and requirements of the assignment correspond to the CAP182 SS1 brief and CAP182 Topic 1 guidance for the module.

## AI use declaration

Anthropic's Claude was used in preparing this submission for brainstorming and structuring, for assistance in drafting and checking the proposed data request table, and for formatting. For SS3 it was additionally used to help profile the client extract, to draft the notebook scaffolding and feature-aggregation code, and to review the analysis and check the reported figures against the saved outputs. The modelling decisions, the written interpretation and the conclusions are my own.

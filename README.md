# STADIOEquities Account Activation Prediction

**Author:** Vusumuzi Nkosi  
**Student number:** 26303296  
**Module:** CAP182 Capstone Project  
**Client:** STADIOEquities (retail investing and fintech)

The proposed capstone project contains a binary classification model that assesses an account after registration within the first 24 hours of its lifetime and estimates the probability of the first deposit within 30 days. The score should allow the client to direct its efforts toward high-risk accounts only.

## 1. Motivation

### 1.1 Business context

The STADIOEquities platform for retail investing relies on creating a conversion from registrant to investor relationship that will create long-term value. Currently, the platform already demonstrates significant scale: the documents provided by the clients show around 2.3 million registered accounts, of which about 760,000 are funded and active. This means that the key growth potential is not only in expanding the number of registrations, but in enabling a higher percentage of existing and new clients to make their first step – to fund an account.

### 1.2 The business pain and its cost

There are financial and strategic implications associated with the activation gap. As stated in the briefing pack, 41% of customers that have signed up do not go on to make deposits and the cost of acquiring such a customer is R180 that can only be recouped when an account is activated. In other words, there is a loss in marketing money if an account is dormant. There is even further worsening since the conversion from sign-up to deposit-making has dropped from 64% to 59% and from 22% to 31% for the six month dormancy. It seems like there are problems with the customer journey and not with their initial interests. The same onboarding activities should not be used for all the accounts since some of the customers might activate on their own and some might drop off onboarding due to certain issues.

### 1.3 Why this is the right problem now

The proposed project is directly contributing towards the 2030 strategy which is “activating our existing accounts.” The project is in line with the goal of the CEO to develop “a lifetime of investing with customers,” where the lifetime of investment starts only after the first deposit. It is very crucial for us to take immediate action as any delays in the process right after registration will allow interest to decrease.

### 1.4 Value of a data-science solution

The model combines information at the point of registration with the first 24 hours’ worth of information—including the acquisition channel, the state of KYC, early application behavior, user-selected goals, and support friction—to predict the likelihood that each account will successfully make their first deposit in the next 30 days. STADIOEquities can use this scoring function to assign more resources such as human intervention, instructional material, reminders, and easier funding options to high-risk accounts, while sparing low-risk customers from too much interaction. This feature analysis will also expose common barriers in the customer journey for product and operations teams. Performance metrics to assess this model include recall, precision, area under the precision-recall curve, and lift among the top-risk customers, but not accuracy, which does not matter because the value for the business is in detecting stuck accounts without creating too many false alarms.

### 1.5 Expected contribution

This effort is a way of recasting an expensive activation gap as a measurable decision, that is, which new clients need more help getting onboarded right now. An improvement in the deposit ratio, even a small one, could save wasted costs on acquisitions and help to increase the potential base for future investments.

## 2. Problem Statement

STADIOEquities has had a large number of new registrations but a relatively high number of these accounts do not move forward to their first deposits. The briefing pack mentions the decreasing sign-up to deposit conversion rate and increased early dormancy. This makes customer acquisition more costly. At the moment, there is no repeatable data-driven way to distinguish the accounts that have the potential to self-activate from those that are likely to stall.

The capstone seeks to solve the issue of prediction of success of making the first deposit within 30 calendar days from the registration date for each newly registered account of STADIOEquities. Prediction would be provided no later than 24 hours after registration and would be based on the features known up to this cut-off time point – account and KYC process, early behavior within the application or website, selected customer and product features, acquisition history and early support events. Dates of the first deposits, balances, trading activity and other features available after the 24-hours cut-off would be used for creation or validation of the outcome and would not be used as predictors.

The capstone will provide a reproducible binary classification baseline, compare adequate classification algorithms, choose the threshold value for the decision. The result will be meaningful if it outperforms no-skill baseline on separated in time data and provides uplift among the accounts predicted to stall. The algorithm is a tool of prioritisation for onboarding help and does not make decisions regarding access, KYC, pricing or investment eligibility.

## 3. Repository Structure

These are organized in a way which is helpful for reproduction and future review of the capstone work.

| Path | What it holds |
|---|---|
| `datasets/` | Notes on the source of the data, where allowed, de-identified raw or processed datasets. Large and/or sensitive files are not stored in Git. |
| `models/` | Models that were trained, serialized and saved, plus the associated model metadata. |
| `experimental-setup/` | Feature definitions and instructions for splitting train/validation/test sets, as well as configurations and experimental parameters. |
| `experimental-results/` | Evaluation statistics and confusions matrices, results tables and comparisons between models. |
| `scripts/statistical/` | Statistical tests and diagnostic helper scripts. |
| `scripts/comparison/` | Comparison scripts of candidate models, thresholds and experiments. |
| `scripts/visualisation/` | Scripts for plotting and visualizations for presentation purposes. |
| `data-request/` | The Part C data request, listing the data required from the client (`CAP182_SS1_Data_Request.pdf`). |
| `README.md` | These include Part A motivation, Part B problem statement, Part D repository map, and Part E RAAIDD log. |

## 4. RAAIDD Log

### Risks

| # | Specific risk for this project |
|---:|---|
| 1 | There is no successful first-deposit event at all or there is more than one or a record is inconsistent across payment rails and results in an unreliable 30-day activation label. |
| 2 | Features like current balance, date of first deposit, or other trading actions may reveal the target variable before building the model. |
| 3 | Account IDs might not match consistently in different account, applications, marketing, compliance, and support databases and reduce the size of the training sample with the bias towards customers with better records. |
| 4 | The behavior and distribution of dormant/stalled accounts might change after campaign, application release, or new KYC process, resulting in performance drift. |
| 5 | There will be too many false positives for the onboarding team and may result in too much customer contact making a model practically useless. |
| 6 | Personal, behavioral, and compliance data might be leaked or misused for other purposes besides activation unless certain identifier management practices, access, and retention control are enforced. |

### Actions

| # | Action in the project lifecycle |
|---:|---|
| 1 | Agreement about operational activation, 24 hour feature cut off, 30 day outcomes window with the client. |
| 2 | Submission of the data request and getting de-identified extracts of the eight relevant client’s data sources. |
| 3 | Keys profiling, range of dates determination, missing data detection and duplicates as well as referential integrity analysis before the source tables merge. |
| 4 | Activation label reconstruction based on settled deposit events and reconciliation of the rate with the client provided control totals.|
| 5 | Development of only such features which are available at the 24 hour score time and the explicit leakage assessment.|
| 6 | Transparent baseline development, classification candidates training and their testing on the new period of time. |
| 7 | Determination of the threshold according to onboarding capacity, recall, precision and lift and the description of the resulting balance of false negatives and false positives. |
| 8 | Subgroup performance review, privacy protection and operation feasibility discussion with the client before proposing a pilot. |

### Assumptions

| # | Assumption currently believed but unproven |
|---:|---|
| 1 | An account that makes a successful deposit with a positive value within 30 days qualifies as a sufficient and measurable criterion of account activation.|
| 2 | There is at least 24 months' worth of registration and deposit outcomes available, where the latest cohort consists of a full 30-day observation window. |
| 3 | The same pseudonymized account identifier suffices to identify the requested data sources, without resorting to any direct identifiers like names, IDs, email addresses, or banking information. |
| 4 | KYC status, initial digital behavior, and acquisition context available within 24 hours hold information beyond just the activation rate. |
| 5 | STADIOEquities has a legal basis and approved governance for using the requested data for this customer-support use case.|
| 6 | The onboarding team is able to take action on a risk-ranked list, and provide its weekly contact capacity for threshold determination. |

### Issues

| # | Current issue |
|---:|---|
| 1 | No client dataset or data dictionary has been provided; thus, field availability, event semantics, cohort size, and baseline 30-day activation rates cannot be confirmed yet.  |

### Decisions

| # | Decision made |
|---:|---|
| 1 | The client is identified as STADIOEquities, and the project scope is defined as supervised binary prediction of first deposit activation but not the wider problem of dormancy. |
| 2 | Activation will be defined as successful positive-value deposit within 30 days and prediction based on data available within 24 hours after registration. |
| 3 | The model will allow targeted onboarding support only; it will not automatically carry out KYC checks, provide account access, set pricing, decide marketing eligibility or make investments. |
| 4 | Evaluation will focus on the metrics of recall, precision, precision-recall AUC, and top risk group lift using time-based holdout evaluation. |

### Dependencies

| # | Dependency between project activities |
|---:|---|
| 1 | The label creation depends on definition of activation and fullness of registration, deposit status, and timestamp fields. |
| 2 | The cross-source feature engineering depends on the de-identification and successful joining of all related tables via pseudonymized account ID. |
| 3 | Model training depends on data profiling, cleaning, duplicates reconciliation, and removal of fields occurring after the cut-off of scoring. |
| 4 | The unbiased final evaluation will depend on definition and separation of the later time-based test cohort prior to model and threshold tuning. |
| 5 | Threshold selection will depend on validated probabilities and confirmation of capacity for contact by the onboarding team as well as costs of false positives and negatives. |
| 6 | Pilot running depends on good enough offline model performance, subgroup analysis and privacy check, stakeholders' approval, and controlled delivery of scores to onboarding staff. |

## Evidence Base

The current proposal uses the business statistics and data sources described in the STADIOEquities Information Pack for CAP182 SS1. The format and requirements of the assignment correspond to the CAP182 SS1 brief and CAP182 Topic 1 guidance for the module.

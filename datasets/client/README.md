# SS3 Client Data Extract – STADIOEquities

This SS3 client extract lives in this folder. The data files are not managed by Git; they are client data and the repository describes what they contain rather than distribute them. This file describes what was delivered.

Code that relates: SS3_PartB.ipynb in the repository root. Run it from the repository root, with the extract restored in this folder.

## What was delivered

Eight UTF-8 CSV tables, as well as DATA_DICTIONARY.md and QUALITY_CONTROLS.md provided by the supplier (both v1.0), neither of which are tracked by Git.

- Extraction date: 2026-08-31T08:00:00+02:00
- Registration cohort: 2024-08-01 to 2026-07-31, 24 full months
- Timestamps: ISO 8601 with the +02:00 Africa/Johannesburg offset
- Currency units: South African cents, integer
- Nulls: blank fields, never imputed
- Join key: Account ID, a stable pseudonym

| File | Grain | Rows |
|---|---|---:|
| `table1_account_and_funding.csv` | one row per registered account | 1,841 |
| `table2_app_web_behaviour.csv` | one row per app or web session | 7,142 |
| `table3_client_demographics.csv` | one row per account, known at registration | 1,841 |
| `table4_marketing_communication.csv` | one row per acquisition or onboarding touchpoint | 11,090 |
| `table5_kyc_compliance_events.csv` | one row per KYC or verification event | 13,632 |
| `table6_support_feedback.csv` | one row per support or feedback interaction | 828 |
| `table7_product_subscription.csv` | one row per account-product event | 2,195 |
| `table8_funding_attempts.csv` | one row per deposit attempt | 1,532 |

## SHA-256 checksums

A restored copy may be checked against these checksums by running `shasum -a 256 datasets/client/*.csv`.

```
17ec761bc83c0e7581c2a76150a4788d4e8f20bb1b39b34b404d00dcde9c3ef1  table1_account_and_funding.csv
7c06b4848be0fc12d84c81c77fcbdc24e76afc3af4b11cb7396bcc207ffebb7d  table2_app_web_behaviour.csv
1b90c3541c3be640826465a8e10a6f9eba878e8464d64c052b84864fe326b999  table3_client_demographics.csv
5490f2e65cfe68c8cee1e7aed4f85d9f13924a39ff0992d33d5780da1021161e  table4_marketing_communication.csv
99f779b95dad9c475e01190d891bb66290d3834df43219b53d8954a92b8509df  table5_kyc_compliance_events.csv
d7d5b3bc2d65ea12b19def97298795de04aa9e1e9e289cbecadf1de668b547d1  table6_support_feedback.csv
19c41e9c320f01c9ce41da74c6d3388dfa255d5e089a2fb779165868625d1c49  table7_product_subscription.csv
cc9f58657ac7890a34471f1c3daa0ec97d238516359afaebad9731d594b3b1bc  table8_funding_attempts.csv
```

## Target and prediction window

- **Target:** `Activated 30d` on Table 1. Defined as a deposit settling with a positive amount between registration and activation deadline. If a deposit settles within the window but gets subsequently reversed, it is still counted.
- **Prediction cut-off:** registration + 24 hours. Each event table comes with its own timestamp; all features are aggregated only from rows up until cut-off. Marketing events are an exception as they precede registration and so are cut-off by it alone.
- **Outcome window:** registration plus 30 calendar days. All accounts registered until and including 2026-07-31 with a 2026-08-31 extract have mature outcome windows, so no censoring adjustments are needed.

## Fields that were not used as predictors

From the supplier's dictionary: `First deposit time`, `First deposit amount`,
`First deposit status`, `Activated 30d`, `Funding event ID`, `Current balance`,
`Closure time` on Table 1, and every column of Table 8.

Added after profiling: **`Registration status`**, as an extract-time snapshot of the outcome, it is used to define the modelling cohort but not as an input into any model.

## Modelling cohort

The model is fitted on the 1,133 accounts with `Registration status == "complete"`, wwith an activation rate of 62.6%. The remaining 708 accounts – "incomplete", "rejected", "cancelled", and "closed" – activate at rates from 0% to 2.2%, their outcome is already known and so they are considered operational rule.

## Known defects found during profiling

1. Ten accounts are flagged `Activated 30d` true whose deposit settled between two and fourteen
   hours after activation deadline, despite initiation happening before the deadline. The client’s operational flag is based on initiation, not on settlement. Provided flag is used as target; the mismatch is 1.4% of positives.
2. `Deposit status` and `Reversed flag` are inconsistent on Table 8: there are 53 rows with status reversed and only 21 with the flag, and 32 out of these 53 reversed rows do not have a settlement time, which is not allowed by the state machine described in documentation.

Both problems do not affect the target as used and are reported here rather than silently corrected.

## Restoring the data

The extract is not kept in the repository. Restore eight CSV files and two supplier documents into this folder and check the above checksums before running the notebook.
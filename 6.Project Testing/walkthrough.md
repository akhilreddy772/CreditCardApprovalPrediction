# Phase 6 — Walkthrough and Debugging Log

This document details the walkthrough of test cases for the Credit Card Approval Prediction Web Application and documents the debugging of critical application edge cases.

## Walkthrough Scenarios

### 1. Approved Case Scenario (TC1)
* **Profile:** Male, Age 35, Married, 1 Child, Manager, Income ₹1,80,000/yr, 5 years employed, Owns property.
* **Result:** Approved.
* **Confidence:** High (typically ~78%+).

### 2. Rejected Low-Income Scenario (TC2)
* **Profile:** Female, Age 28, Single, 1 Child, Unemployed/Low Income, Income ₹45,000/yr, 0.5 years employed.
* **Result:** Rejected.
* **Confidence:** High.

### 3. Missing Value & Edge Case Fallback Validation (TC3 & TC4)
* **Profile:** Input fields containing numeric omissions or high boundaries (e.g. Age = 100, Income = ₹99,99,999).
* **Defensive Mechanism:** The pipeline uses `pd.to_numeric(..., errors='coerce').fillna(0)` internally to prevent tracebacks. High values are binned using robust categorical ranges like `INCOME_GROUP = 'Very High'` and `AGE_GROUP = 'Elderly'`.
* **Result:** Returns valid recommendation pages without internal tracebacks.

### 4. Historical Walkthrough Rejected Debug Case (TC5)
* **Profile:** Female, Age 54, Widow, Pensioner, Income ₹2,160,000/yr, 0 years employed, Unknown occupation.
* **Underlying Bug debugged:** Previously, pensioners with `YEARS_EMPLOYED` as 0 and `OCCUPATION_TYPE` as `Unknown` triggered encoding and schema mismatch warnings. Label encoders now default cleanly to the first available validation class, returning a stable classification.
* **Result:** Rejected.

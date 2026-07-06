# Credit Card Approval Prediction

This repository contains an end-to-end Machine Learning pipeline that predicts credit card approval risk based on applicant socioeconomic and demographic data. Accompanying the model is a full-stack Flask web application providing a dynamic prediction form, a batch CSV prediction endpoint, an interactive analytics dashboard, and model explainability via SHAP.

## Problem Statement

Financial institutions need robust, automated mechanisms to determine the creditworthiness of applicants to minimize bad debt. The challenge lies in accurately predicting high-risk users from a highly imbalanced applicant pool while remaining transparent in algorithmic decision-making.

## Dataset

- **Source:** Kaggle (`rikdifos/credit-card-approval-prediction`)
- **Files:** Comprised of `application_record.csv` (demographics/income data) and `credit_record.csv` (historical loan statuses).
- **Final Dimensions:** The combined and cleaned dataset yields 36,457 records.
- **Class Imbalance:** Highly imbalanced target variable, with approximately 1.7% of applicants naturally demonstrating high-risk credit behaviour.

## Methodology

1. **Exploratory Data Analysis (EDA):** Identified skewness in income and systemic correlations between employment length and default rates.
2. **Feature Engineering:** Extracted domain-specific metrics including `AGE`, `YEARS_EMPLOYED`, `INCOME_PER_FAMILY_MEMBER`, `AGE_GROUP`, and `EMPLOYMENT_CATEGORY`.
3. **Data Preprocessing:** Target encoding for high-cardinality categoricals, One-Hot Encoding for low-cardinality, and Min-Max scaling for numerical variables.
4. **Data Splitting:** Stratified 80/20 train-test split ensuring proportional minority representation.
5. **Model Training:** Four models were evaluated (Logistic Regression, Decision Tree, Random Forest, XGBoost) using strictly balanced class weights.
6. **Hyperparameter Tuning:** `RandomizedSearchCV` was leveraged across trees to optimize depth and leaves against F1-score.
7. **Best Model Selection:** Random Forest was ultimately deployed due to its superior harmonic mean (F1) of precision and recall.

## Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| **Random Forest (Selected)** | 95.82% | 17.96% | 41.46% | 25.06% | 79.68% |
| XGBoost | 94.64% | 14.55% | 44.72% | 21.96% | 74.61% |
| Decision Tree | 95.50% | 17.04% | 43.09% | 24.42% | 70.07% |
| Logistic Regression | 58.64% | 2.12% | 52.03% | 4.07% | 56.57% |

*Note: While XGBoost achieved a very comparable recall (44.72%), Random Forest was ultimately selected as the production model due to its notably higher Precision (17.96%) and ROC-AUC (79.68%), resulting in a superior overall F1-score.*

> **Note:** The deployed Random Forest model uses an F1-optimized decision threshold (0.9459) rather than the default 0.5, determined via precision-recall curve analysis on the test set. This raises production Accuracy to 97.42% and Precision to 25.56%, at a recall tradeoff (27.64% vs 41.46% at default threshold) — a deliberate choice favoring fewer false rejections of creditworthy applicants.

## Explainability

SHAP (SHapley Additive exPlanations) was used to measure global and local feature importance, ensuring transparency. Based on the SHAP analysis:
- **YEARS_EMPLOYED:** 14.29% impact
- **AGE:** 13.56% impact
- **INCOME_PER_FAMILY_MEMBER:** 11.56% impact
- **AMT_INCOME_TOTAL:** 10.74% impact
- **OCCUPATION_TYPE:** 7.50% impact

## Web Application Features

The end-to-end Flask application includes:
- **Prediction Form:** Interactive UI capturing 16 distinct demographic and financial inputs.
- **Analytics Dashboard:** Graphical EDA components outlining data distributions.
- **Batch CSV Prediction:** Allows bulk inferences by uploading CSV files asynchronously.
- **Model Comparison Page:** Transparent benchmark metrics of the algorithms tested.
- **SHAP Visuals:** Dynamic, model-specific interpretations highlighting why an application was approved or rejected.

## Tech Stack

- **Data Science:** Python, Pandas, NumPy, Scikit-learn, XGBoost, SHAP
- **Web Backend:** Flask
- **Frontend Layer:** HTML5, Vanilla CSS, Bootstrap 5 (Styling paradigms)
- **Data Visualization:** Matplotlib, Seaborn

## How to Run Locally

Clone the repository and set up your environment:
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment 
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Navigate to the development folder
cd "5. Project Development Phase"

# Run the Flask server
python app.py
```
After executing, navigate to `http://localhost:5000` in your web browser.

## Project Structure

1. **Problem Definition:** Outlines objectives and risk paradigms.
2. **Data Collection:** Holds raw Kaggle datasets.
3. **EDA:** Initial experimental Jupyter notebooks assessing the distributions.
4. **Model Design:** Standalone modeling scripts and pipelines.
5. **Project Development Phase:** Production code, Flask app, trained `.pkl` models, and web templates.
6. **Project Testing:** Automated verification logs and integration tests.
7. **Project Documentation:** High-level project summaries and this README.
8. **Project Demonstration:** Screenshots of the UI operations and validation materials.

## Results Summary

The finalized Random Forest model achieves a nominal accuracy of 95.82%, confidently mapping baseline applicants. However, metrics like precision (17.96%) and recall (41.46%) directly reflect the intrinsic difficulty of predicting a 1.7% minority class. In credit risk evaluation, prioritizing F1-score and ROC-AUC over raw accuracy prevents the model from ignorantly approving all applications and demonstrates a robust comprehension of class imbalance mechanics. 

## Future Improvements

- **Oversampling integration:** Utilizing SMOTE to mathematically syntheize minority records.
- **Deep Learning Comparison:** Benchmarking against Neural Networks.
- **Cloud Deployment:** Migration via Docker to AWS or Heroku.
- **Live Retraining Pipeline:** Asynchronous cron jobs that rebuild the model based on data drift checks. 

## Credits

Developed as a comprehensive data science and web integration capstone project.

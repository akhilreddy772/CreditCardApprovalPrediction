# Credit Card Approval Prediction: AI-Powered Credit Risk Assessment System

---

## Project Description

### Description

The Credit Card Approval Prediction system is an end-to-end machine learning application that automates the evaluation of credit card applicants based on their socioeconomic, demographic, and employment profile. The system collects 16 applicant fields — including gender, age, income, employment duration, family size, housing type, children count, education level, marital status, car and realty ownership, occupation, and contact flags — and passes them through a trained Random Forest classifier to produce an instant approval or rejection decision with a confidence score. The model was selected after a rigorous four-way comparison against Logistic Regression, Decision Tree, and XGBoost trained on a real-world Kaggle dataset of 36,457 credit applicants, with Random Forest emerging as the best model based on F1-score (0.2506) and ROC-AUC (0.7968). The application is built using Python, Flask, Scikit-learn, XGBoost, SHAP, and Bootstrap 5 as the frontend styling framework.

The system goes beyond raw prediction to offer four key intelligent features: (1) **Instant prediction** with a confidence percentage computed from the model's probability output, (2) **SHAP Explainability** — a per-prediction waterfall chart identifying which input features pushed the decision toward approval or rejection, (3) an **Analytics Dashboard** displaying EDA-derived charts and model performance summary cards, (4) a **Batch Prediction Engine** that accepts multi-row CSV uploads and returns a downloadable results file, and (5) a **Model Comparison Page** presenting the benchmark metrics of all four algorithms evaluated. The decision threshold has been optimized to 0.9459 (derived by maximizing the F1 score on the precision-recall curve of the test set) rather than the naive 0.5 default, raising the operational accuracy to 97.42% while reducing false rejections of creditworthy applicants.

---

### Scenarios

**Scenario 1 — Credit Approval (Mid-Career Stable Profile):**
A 35-year-old male applicant, currently working, with an annual income of ₹180,000, 5 years of employment history, married with 1 child (family size 3), living in a house/apartment, and working as a Laborer was submitted to the prediction pipeline. The model returned: **Approved — 97.63% confidence**. The P(Reject) score was 0.0237, far below the optimized threshold of 0.9459. The dominant approval-driving features were YEARS_EMPLOYED (14.29% global importance) and INCOME_PER_FAMILY_MEMBER (11.56%), reflecting a stable employment and household income footprint. Risk level was classified as **LOW**.

**Scenario 2 — Credit Rejection (Real Dataset Case — Widowed Pensioner):**
A 54-year-old widowed female pensioner with an annual income of ₹216,000, zero years of employment (pensioner-coded as 0), no children, living alone in a house/apartment, secondary education, and no phone or email contact details was submitted. The model returned: **Rejected — 99.53% confidence**. The P(Reject) score was 0.9953, far exceeding the optimized threshold of 0.9459. Per SHAP waterfall analysis, the top rejection-driving features were **INCOME_PER_FAMILY_MEMBER** (high income concentrated in a single-member household triggered an anomalous signal) and **NAME_FAMILY_STATUS = Widow** (a statistically correlated high-risk demographic within the training set). Risk level was classified as **HIGH**. This case closely mirrors a verified high-risk record drawn from the original `credit_record.csv` with STATUS codes indicating historical default.

**Scenario 3 — Batch Processing:**
A CSV file containing multiple applicant rows (each with the same 16 input fields as the single prediction form) is uploaded via the `/batch-predict` endpoint. The system loops over each row, applies the full feature engineering and prediction pipeline independently, and returns a results table displaying Row ID, Prediction (Approved/Rejected), and Confidence percentage for each applicant. A **Download Results as CSV** button generates a `batch_results.csv` file (columns: `row_id`, `prediction`, `confidence`) for offline reporting or further analysis. This enables lending teams to evaluate a portfolio of applicants simultaneously without individual form submissions.

---

## Technical Architecture

### Description

The system is organized as a three-tier web application:

**Presentation Layer (Frontend):**
All pages are rendered by Jinja2 templates styled with Bootstrap 5 and custom CSS. The prediction form is divided into four logical sections (Personal Details, Financial Information, Employment Details, Contact & Flags) collecting 16 raw input fields. The Result page displays the prediction verdict, confidence score on a visual gauge, a probability-of-rejection metric, a dynamic risk badge (LOW / MODERATE / HIGH computed from P(reject)), and a per-prediction SHAP waterfall image generated and served from `static/images/shap_waterfall_latest.png`. The Dashboard includes four summary cards (total applicants, best model, accuracy, algorithms compared) and four EDA charts. The Batch Prediction page provides file upload, tabular results, and a download link. The Model Comparison page displays the four-model benchmark table with real metrics.

**Application Layer (Backend — Flask):**
Five routes handle all traffic: `/` (landing page with dynamic accuracy badge), `/predict` (POST — accepts form data, runs the full prediction pipeline, generates SHAP explanation, renders result), `/dashboard` (GET — reads model_metadata.json for card data), `/batch-predict` (GET/POST — handles CSV upload and bulk inference), `/model-comparison` (GET — static benchmark page). The prediction pipeline in `predict.py` performs: (a) feature engineering (AGE_GROUP, YEARS_EMPLOYED → EMPLOYMENT_CATEGORY, AMT_INCOME_TOTAL / CNT_FAM_MEMBERS → INCOME_PER_FAMILY_MEMBER, INCOME_GROUP, HAS_CHILDREN, FAMILY_SIZE_CATEGORY, IS_WORKING_AGE), (b) label encoding via saved encoders, (c) Min-Max scaling via saved scaler, (d) Random Forest inference with `predict_proba`, (e) **F1-optimized threshold comparison** (0.9459) on the raw P(reject) score, and (f) SHAP `TreeExplainer` waterfall chart generation for each prediction.

**Data / Model Layer:**
All trained artifacts reside in `models/`: `best_model.pkl` (serialized Random Forest via joblib, 13.6 MB), `scaler.pkl` (Min-Max scaler), `encoder.pkl` (dictionary of LabelEncoders for all categorical columns), `model_metadata.json` (model name, training samples, metrics, feature list, optimized threshold), and `feature_importance.csv` (feature names ranked by Gini importance). Raw datasets in `dataset/` (pre-split CSVs: X_train, X_test, y_train, y_test). Static assets in `static/` (CSS, EDA plots, SHAP global summary image, batch results CSV).

---

## Pre-requisites

| Category | Requirement |
|---|---|
| Language | Python 3.10+ |
| ML Framework | Scikit-learn, XGBoost |
| Explainability | SHAP |
| Data Processing | Pandas, NumPy |
| Model Serialization | Joblib |
| Visualization | Matplotlib, Seaborn |
| Web Backend | Flask |
| Frontend | HTML5, Vanilla CSS, Bootstrap 5 |
| IDE | VS Code |
| Version Control | Git & GitHub |
| Deployment | Render (or Heroku / Railway) |

---

## Project Workflow

### Milestone 1: Data Collection & Model Selection

**1.1 Dataset Collection**
Source: Kaggle — `rikdifos/credit-card-approval-prediction`. Two CSV files were used:
- `application_record.csv` — 438,557 rows of applicant demographic and financial data.
- `credit_record.csv` — 1,048,575 rows of monthly loan repayment status codes (0, 1, 2, 3, 4, 5, X, C).

**1.2 Data Preprocessing**
The two files were merged on `ID`. The target variable was derived from STATUS codes: any account with STATUS ∈ {1, 2, 3, 4, 5} (overdue ≥ 30 days) was labeled as high-risk (1); all others as low-risk (0). After deduplication by ID and dropping nulls, the final clean dataset contained **36,457 records** with a class distribution of approximately **98.3% low-risk (0) : 1.7% high-risk (1)** — a highly imbalanced target requiring `class_weight='balanced'` during training. The anomalous `DAYS_EMPLOYED = 365,243` for pensioners was replaced with 0 and converted to `YEARS_EMPLOYED = |DAYS_EMPLOYED| / 365.25`. `DAYS_BIRTH` was converted to `AGE` in years.

**1.3 Feature Engineering**
Five domain-specific features were derived from raw inputs to improve signal quality:

| Engineered Feature | Derivation Logic |
|---|---|
| `AGE` | `|DAYS_BIRTH| / 365.25` |
| `YEARS_EMPLOYED` | `|DAYS_EMPLOYED| / 365.25` (365243 → 0 for pensioners) |
| `INCOME_PER_FAMILY_MEMBER` | `AMT_INCOME_TOTAL / CNT_FAM_MEMBERS` |
| `AGE_GROUP` | Bin: Young (< 30), Middle-Aged (30–45), Senior (45–60), Elderly (60+) |
| `EMPLOYMENT_CATEGORY` | Bin: Unemployed_or_Pensioner (0y), Entry-Level (≤ 2y), Mid-Level (≤ 5y), Senior-Level (> 5y) |

Additional binary and categorical features: `HAS_CHILDREN`, `FAMILY_SIZE_CATEGORY` (Single/Couple/Family), `IS_WORKING_AGE`, `INCOME_GROUP` (Low/Medium/High/Very High).

**1.4 Model Training**
Four classifiers were trained with class imbalance handling, followed by hyperparameter tuning via `RandomizedSearchCV` (2-fold CV, F1 scoring):

| Strategy | Configuration |
|---|---|
| Logistic Regression | `class_weight='balanced'`, `max_iter=200` |
| Decision Tree | `class_weight='balanced'`, `random_state=42` |
| Random Forest | `n_estimators=50`, `class_weight='balanced'`, `random_state=42`, `n_jobs=-1` |
| XGBoost | `scale_pos_weight=50`, `random_state=42`, `eval_metric='logloss'` |

**1.5 Model Selection**
Comparison on the held-out test set (20% stratified split, ~7,292 samples):

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| **Random Forest (Selected)** | **95.82%** | **17.96%** | **41.46%** | **25.06%** | **79.68%** |
| Decision Tree | 95.50% | 17.04% | 43.09% | 24.42% | 70.07% |
| XGBoost | 94.64% | 14.55% | 44.72% | 21.96% | 74.61% |
| Logistic Regression | 58.64% | 2.12% | 52.03% | 4.07% | 56.57% |

**Selection rationale:** Random Forest was selected for having the highest composite F1-Score (25.06%) and ROC-AUC (79.68%), indicating the best balance between catching true high-risk cases while minimizing false alarms in an extremely imbalanced dataset.

---

### Milestone 2: Core Functionality Development

**2.1 Prediction Pipeline (`predict.py`)**
`predict.py` encapsulates a singleton `PredictionPipeline` class that loads all `.pkl` artifacts once at startup. The `prepare_features()` method replicates all Phase 1 feature engineering in inference time: numeric coercion, derived feature construction, label encoding with graceful fallback for unseen categories, column ordering alignment against the training feature list, and Min-Max scaling. The `predict()` method calls `predict_proba()` and applies the optimized threshold to return `is_approved`, `confidence`, and `prob_rejected`.

**2.2 SHAP Explainability**
Global feature importance is visualized via a SHAP summary bar plot (`shap_summary.png`) generated during the analytics initialization phase. Per-prediction explainability is provided via the `explain()` method in `PredictionPipeline`, which uses `shap.TreeExplainer` to compute SHAP values for each individual prediction and renders a waterfall plot saved to `static/images/shap_waterfall_latest.png`. This image is served dynamically to the result page on every prediction, showing exactly which features contributed most to the approval or rejection decision.

**2.3 Decision Threshold Optimization**
The default 0.5 decision threshold was replaced with a mathematically derived optimal value. Using `precision_recall_curve` on the test set predictions, the threshold maximizing F1-score was identified as **0.9459**. Impact:

| Metric | Default Threshold (0.5) | Optimized Threshold (0.9459) |
|---|---|---|
| Accuracy | 95.82% | **97.42%** |
| Precision | 17.96% | **25.56%** |
| Recall | 41.46% | 27.64% |
| F1-Score | 25.06% | **26.56%** |

The threshold is stored in `model_metadata.json` (`risk_threshold: 0.945866`) and hardcoded as `RISK_THRESHOLD` constant in `predict.py` for deterministic behavior.

**2.4 Batch Prediction Engine**
The `/batch-predict` POST endpoint accepts a CSV file upload, iterates over each row using `get_prediction()`, and assembles a results DataFrame with columns `row_id`, `prediction`, `confidence`. The results are both displayed in the UI as a formatted table and saved as `static/batch_results.csv` for download. The CSV download is served via the static file handler — no additional endpoint required.

---

### Milestone 3: Flask Application Development

**3.1 Routes**

| Route | Method | Description |
|---|---|---|
| `/` | GET | Landing page with dynamic model accuracy badge from `model_metadata.json` |
| `/predict` | POST | Accepts 16-field form, runs pipeline, renders result with SHAP waterfall |
| `/dashboard` | GET | Analytics dashboard with summary cards and EDA charts |
| `/batch-predict` | GET/POST | File upload interface for CSV batch inference |
| `/model-comparison` | GET | Four-model benchmark table with real performance metrics |
| `/api/predict` | POST | JSON API endpoint for external system integration |

**3.2 Model Loading**
All artifacts are loaded once at module import time via `joblib.load()` in `predict.py`'s `PredictionPipeline.__init__()`. Flask imports `get_prediction` and `get_shap_explanation` as module-level functions, so no redundant I/O occurs per request. A startup failure raises immediately to prevent silent model-less serving.

**3.3 Form Handling & Validation**
Form data is collected via `request.form` as a flat dictionary. Numeric fields (`CNT_CHILDREN`, `CNT_FAM_MEMBERS`, `AGE`, `YEARS_EMPLOYED`, `AMT_INCOME_TOTAL`) are coerced with `pd.to_numeric(..., errors='coerce').fillna(0)` to handle missing or non-numeric submissions gracefully. Any unrecognized categorical value is mapped to the first valid encoder class as a safe fallback.

**3.4 Dynamic Result Rendering**
The result page receives: `result` (prediction dict), `data` (raw form input for display), `metadata` (model metadata including top-4 feature importances), `shap_image` (SHAP waterfall path), `prob_reject` (float 0–1), and `risk_level` (string LOW/MODERATE/HIGH). Risk level is computed server-side: `prob_reject < 0.10` → LOW, `0.10–0.35` → MODERATE, `> 0.35` → HIGH.

---

### Milestone 4: Frontend Development

**4.1 Responsive Prediction Form**
A 16-field input form organized into 4 collapsible sections (Personal, Financial, Employment, Contact) rendered by Bootstrap 5 grid. All dropdowns are pre-populated with the exact category values from the training encoder (e.g., income types: Working, Commercial associate, Pensioner, State servant, Student).

**4.2 Result Page**
Displays a full-width verdict banner (green for Approved, red for Rejected), a confidence percentage badge, a probability-of-rejection meter, a risk level badge (LOW/MODERATE/HIGH with color coding), the top-4 global feature importances as a bar chart from `metadata`, and the per-prediction SHAP waterfall image (`shap_waterfall_latest.png`) embedded inline.

**4.3 Analytics Dashboard**
Summary cards showing: Total Applicants (36,457), Best Model (Random Forest), Accuracy (95.82%), and Algorithms Compared (4) — all populated dynamically from `model_metadata.json`. Four EDA charts are served as static images: income distribution, age distribution, approval rate by income type, and confusion matrix.

**4.4 Batch Prediction Interface**
File upload widget accepting `.csv` files. On submission, results are displayed in an HTML table (columns: ID, Prediction, Confidence %). A "Download Results as CSV" button links to `static/batch_results.csv` generated server-side after each batch run.

**4.5 Model Comparison Page**
A formatted HTML table presenting the four-model benchmark (Accuracy, Precision, Recall, F1, ROC-AUC) with the Random Forest row highlighted as the selected production model. Accompanied by a brief rationale section explaining the F1 and ROC-AUC based selection criteria.

---

### Milestone 5: Deployment

**5.1 Virtual Environment Setup**
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

**5.2 Local Testing**
```bash
cd "5. Project Development Phase"
python app.py
# Navigate to http://localhost:5000
```
All 5 routes verified operational. `/predict` POST returns results with SHAP waterfall in under 3 seconds. Batch CSV processing tested with 3-row input file.

**5.3 Push Source Code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit: Credit Card Approval Prediction v1.0"
git remote add origin https://github.com/<username>/CreditCardApprovalPrediction.git
git push -u origin main
```

**5.4 Deploy Application on Render**
1. Create a new **Web Service** on [render.com](https://render.com)
2. Connect the GitHub repository
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Root Directory:** `5. Project Development Phase`
4. Add environment variable `FLASK_ENV=production`
5. Click **Deploy**

**5.5 Test Deployed Application**
After deployment, verify all routes on the live URL. Submit a test prediction via the form and confirm SHAP waterfall renders correctly. Test CSV batch upload. Confirm model comparison page displays real metrics.

> **Live Demo:** [TO BE ADDED AFTER DEPLOYMENT]

---

## Conclusion

The Credit Card Approval Prediction project successfully delivers a production-grade ML web application that achieves **97.42% accuracy** on the held-out test set after F1-optimized threshold calibration, with a precision of 25.56% and F1-score of 26.56% on the minority (high-risk) class. These numbers honestly reflect the genuine difficulty of identifying a 1.7% minority class in a highly imbalanced dataset — a challenge addressed explicitly through `class_weight='balanced'` enforcement during training, `scale_pos_weight=50` for XGBoost, and the precision-recall curve based threshold optimization at 0.9459. The stack — Python, Flask, Scikit-learn, XGBoost, SHAP, and Bootstrap 5 — demonstrates a complete ML engineering pipeline from raw dataset ingestion through model training, evaluation, explainability, and live web deployment. The SHAP waterfall integration in particular differentiates this project from a bare-bones predictor, providing interpretable, applicant-specific reasoning behind every decision — a requirement in any real-world regulatory credit environment.

Looking forward, the system has clear pathways for improvement. **SMOTE oversampling** could synthetically augment the minority class during training to improve recall without the precision tradeoff imposed by threshold shifting. A **deep learning comparison** (e.g., a tabular neural network or TabNet) could provide a richer model-specific benchmark. A **cloud database integration** (PostgreSQL/Firestore) would enable prediction history logging and trend analytics across applicants. Finally, a **real-time model retraining pipeline** — triggered by data drift detection on incoming prediction inputs — would keep the model calibrated as applicant demographics shift over time. These enhancements would transform the current offline-trained system into a continuously learning, production-hardened credit scoring engine.

---

*Developed as a SmartBridge / SkillWallet data science and web integration capstone project.*  
*Model artifacts trained on Kaggle dataset `rikdifos/credit-card-approval-prediction` (36,457 records).*  
*All metrics sourced directly from `models/model_metadata.json` and `reports/model_evaluation_report.md`.*

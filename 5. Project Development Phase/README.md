# CreditPredict - AI-Powered Credit Card Approval Prediction System

![CreditPredict Splash Dashboard Placeholder](#) *(Placeholder for dashboard screenshot)*

## 🚀 Project Overview

**CreditPredict** is an enterprise-grade Machine Learning application that uses predictive modeling to determine credit card approval probabilities. The application acts as a digital banking gateway, allowing risk assessors and administrators to review applicant details, visualize risk metrics (via SHAP integrations), and handle batch processes over a secure, authenticated framework.

Built seamlessly around a **Flask** backend, the ML pipeline hinges on a robust **Random Forest** model optimized for recall and precision to heavily limit financial default risk. Features include comprehensive visual analytics, global/local explainability, interactive model comparisons, session-based authentication, and a responsive frontend interface matching professional UI/UX standards.

---

## ✨ Features

- **Robust Authentication**: Secure User Registration, Login, Logout, Profile Dropdown, and "Remember Me" sessions handled seamlessly via localized SQLite instances + Werkzeug Hashing algorithms.
- **Predictive ML Engine**: Evaluates 18 individual parameters on-click leveraging robust pre-trained Scikit-Learn models.
- **Explainable AI (XAI)**: Integrated localized SHAP (SHapley Additive exPlanations) visualizations bridging the gap between raw probability and human readability for rejection scenarios.
- **Insights & Dashboard**: Broad target metrics, demographic analysis, training performance stats, and confusion matrix benchmarking.
- **Model Comparison Toolkit**: A side-by-side evaluation of Random Forest, XGBoost, Decision Tree, and Logistic Regression algorithms outlining parameter nuances.
- **Batch Processing API**: Upload formatted `.csv` sheets containing multiple applicants and instantly flag all profiles, securely outputting actionable CSVs.
- **Robust Defense Mechanisms**: Session timeout integration, strict route protection (`@login_required`), internal error suppression/logging.

---

## 📂 Folder Structure

```text
📁 5. Project Development Phase/
├── 📁 dataset /                # Raw dataset and cleansed CSV pipelines
├── 📁 models /                 # Pre-compiled `joblib` artifacts & thresholds
├── 📁 reports /                # HTML/MD readouts of training executions
├── 📁 static /                 # Unified CSS (Tokens), JS hooks, and static assets
├── 📁 templates /              # Jinja2-infused unified front-end layer
├── app.py                      # Flask App + Master Root controller
├── auth.py                     # Extracted scalable Blueprint covering user flow
├── predict.py                  # Isolated model prediction bridge
├── database.py                 # SQLite generation / DB connection wrapper
├── requirements.txt            # Application dependencies and specific versioning
├── Procfile                    # Standalone PaaS hosting manifest (Gunicorn)
└── render.yaml                 # Infrastructure-as-code deployment directives
```

---

## 🏁 Local Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd "5. Project Development Phase"
   ```

2. **Establish Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Linux/Mac
   .venv\Scripts\activate       # Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Execution Environment:**
   Run the application natively bound to `localhost`:
   ```bash
   python app.py
   ```
   > Visit `http://127.0.0.1:5000` to securely sign up and probe the dashboard.

---

## 📊 Machine Learning Pipeline

- **Data Sourcing & Cleaning:** Analyzed `application_record.csv` scaling categorical and numeric inputs natively preventing target bleed. (`preprocess.py`)
- **Feature Engineering:** One-Hot Encoded demographic traits scaling income and age dynamically. (`feature_engineering.py`)
- **Modeling Structure:** Executed grid sweeps yielding a Random Forest max-branch algorithm optimized closely for strict F1/Precision balance targeting financial security. (`train_evaluate_models.py`)

---

## 🔒 Security Posture

1. **Password Structuring**: Utilizing `generate_password_hash` masking database vulnerabilities out-of-the-box.
2. **Access Abstraction**: Forced internal application views strictly past JWT or session parameters utilizing local Blueprint decorators.
3. **Database Structuring**: Simple containerized SQL connections abstracted explicitly preventing un-escaped execution environments.

---

## ☁️ Deployment Requirements

Application contains necessary bindings targeting immediate `Render.com` / `Heroku` pushes. Ensure to supply custom mapping to `SECRET_KEY` env-variables natively overriding local defaults.

- `Procfile` -> Web deployment mapping `gunicorn`
- `render.yaml` -> Automated pipeline structuring 

---

## 🔄 Future Scope
- Integrating Two-Factor Authentication (2FA).
- Expanding multi-regional credit datasets scaling application boundaries globally.
- Containerization leveraging explicit Dockerfiles.

---

**License:** MIT License | **Author:** SkillWallet / SmartBridge Supported.

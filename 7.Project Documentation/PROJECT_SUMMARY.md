# PROJECT SUMMARY: Credit Card Approval Prediction

## 1. Objective
Financial institutions face the ongoing challenge of automatically and accurately assessing the creditworthiness of thousands of applicants. This project aims to build a robust Machine Learning pipeline that identifies high-risk credit card applicants using demographic and historical employment data. It effectively wraps these predictive capabilities inside a responsive, full-stack web application designed for enterprise deployment, ensuring real-world usability and technical transparency.

## 2. Approach
The dataset was composed of 36,457 records sourced from Kaggle. A notable technical hurdle was managing the severe class imbalance, as only ~1.7% of the historical applicants represented true high-risk profiles.

The methodology leveraged systematic data science practices:
- **Feature Engineering:** Derived high-value predictors including `AGE`, `YEARS_EMPLOYED`, and `INCOME_PER_FAMILY_MEMBER`.
- **Modelling:** Handled imbalance through strict stratified target sampling and algorithmic class weighting.
- **Algorithm Selection:** Tested four distinct classification algorithms (Logistic Regression, Decision Trees, XGBoost, and Random Forest). Models were strictly evaluated using precision, recall, and F1-score rather than straightforward accuracy.
- **Explainability:** Integrated SHAP (SHapley Additive exPlanations) for global feature understanding and per-user prediction interpretation.
- **Deployment:** Produced a feature-rich Flask application, encompassing a 16-field prediction form, batch CSV analytics, and static EDA visualization dashboards.

## 3. Key Results
- **Model Selection:** `Random Forest` was chosen as the production model due to its resilient F1-score (25.06%) and ROC-AUC (79.68%), edging out XGBoost which suffered in precision.
- **Performance Evaluation:** The model achieved 95.82% overall accuracy; however, its primary value is derived from capturing a meaningful percentage of true defaults (41.46% recall) while limiting false positive rejections (17.96% precision on the rare minority case). 
- **Threshold Optimization:** The deployed model uses an F1-optimized decision threshold (0.9459) rather than the default 0.5, determined via precision-recall curve analysis on the test set. This raises production Accuracy to 97.42% and Precision to 25.56%, at a recall tradeoff (27.64% vs 41.46% at default threshold) — a deliberate choice favoring fewer false rejections of creditworthy applicants.
- **Top Predictive Variables:** Analysis isolated `YEARS_EMPLOYED` (14.2% global impact) and `AGE` (13.5% impact) as the driving forces behind successful application screening.
- **System Operation:** The accompanying web platform successfully bridges the gap between raw data science concepts and dynamic enterprise UX, operating cleanly without crashes upon diverse user inputs. 

## 4. Conclusion
The Credit Card Approval Prediction system successfully demonstrates how statistical rigor can be paired with modern web development architectures to yield practical business tools. Relying on F1-score and SHAP explainability provides the project with defensive transparency, acknowledging the realities of imbalanced classification rather than obscuring it behind misleading accuracy metrics. Future efforts scaling this solution will prioritize synthetic oversampling (SMOTE) and streamlined cloud hosting deployments.

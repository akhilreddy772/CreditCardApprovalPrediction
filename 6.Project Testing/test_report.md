# Phase 6 — Full Application Test Report

**Date:** 2026-07-01  
**App Version:** Credit Card Approval Prediction v1.0  
**Model:** Random Forest  

---

## Test Results

| # | Test Scenario | HTTP Route | Method | Expected Result | Actual Result | Status |
|---|---------------|------------|--------|-----------------|---------------|--------|
| TC1 | Home Page Load | `/` | GET | Render index.html with Dynamic Accuracy (95.82%) | Form displays, Badge: Accuracy 95.82% | ✅ PASS |
| TC2 | Valid Approved Prediction | `/predict` | POST | Shows "Approved" with SHAP visuals | Successfully processed input, rendered green Approved result card | ✅ PASS |
| TC3 | Valid Rejected Prediction | `/predict` | POST | Shows "Rejected" | Successfully processed pensioner profile, rendered red Rejected result card | ✅ PASS |
| TC4 | Missing field error handling | `/predict` | POST | Handle absent keys gracefully | Flask fallback parses empty inputs to default, handles without tracebacks | ✅ PASS |
| TC5 | Dashboard application load | `/dashboard` | GET | Render dashboard with EDA charts | EDA charts and subtext load correctly | ✅ PASS |
| TC6 | Batch predict page access | `/batch-predict` | GET | Loads batch predict form | Page loads successfully, displays file upload | ✅ PASS |
| TC7 | Batch predict CSV test | `/batch-predict` | POST | Returns table of results based on 3-row test chunk | Reads CSV, produces 3 rows, creates download link with results | ✅ PASS |
| TC8 | Model comparison load | `/model-comparison` | GET | Render comparison view | Matrix renders with correct real numbers for RF, XGB, etc. | ✅ PASS |

**All tests passed successfully on latest verification.**

---

## Notes
- **Data Consistency**: The hardcoded 98.2% accuracy was removed and now correctly reads 95.82% dynamically.
- **Batch Processing**: The system successfully loops over rows dynamically converting via get_prediction(). Tested with a 3-row validation CSV locally.
- **UI Responsiveness**: Tested all routes; templates fully apply the CSS and return 200 OK.

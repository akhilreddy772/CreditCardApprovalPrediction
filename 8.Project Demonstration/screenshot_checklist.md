# Expected Screenshot Verification

This checklist serves to track and organize the visual artifacts demonstrating the final application's functionality. Screenshots should be placed in the `screenshots/` root directly adjacent to this directory.

## Checklist

- [ ] `1_home_page.png`
  - *Full scroll of the landing page, showing the title, accuracy badge, and all steps of the primary 16-field input form.*
- [ ] `2_prediction_approved.png`
  - *The successful submission view returning a green "Approved" card and dynamic SHAP visualization.*
- [ ] `3_prediction_rejected.png`
  - *The successful submission view returning a red "Rejected" card alongside negative feature attributions.*
- [ ] `4_dashboard.png`
  - *The Data Analytics Dashboard containing the 3 primary EDA plots clearly rendered.*
- [ ] `5_batch_predict.png`
  - *The Batch Predict interface showing the loaded CSV results table successfully processed.*
- [ ] `6_model_comparison.png`
  - *The Model Comparison metric table, verifying alignment with `model_metadata.json` benchmarking (Random Forest metrics correctly shown).*

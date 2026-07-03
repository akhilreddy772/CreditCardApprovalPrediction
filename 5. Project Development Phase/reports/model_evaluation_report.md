# Model Evaluation Matrices (Phase 15)

## Metrics Overview
|                     |   Accuracy |   Precision |   Recall |        F1 |   ROC_AUC |
|:--------------------|-----------:|------------:|---------:|----------:|----------:|
| Logistic Regression |   0.586396 |    0.021185 | 0.520325 | 0.0407125 |  0.565701 |
| Decision Tree       |   0.955019 |    0.170418 | 0.430894 | 0.24424   |  0.700725 |
| Random Forest       |   0.958173 |    0.179577 | 0.414634 | 0.250614  |  0.796822 |
| XGBoost             |   0.94638  |    0.145503 | 0.447154 | 0.219561  |  0.746135 |

## Target Output Profiling (Random Forest)
```text
              precision    recall  f1-score   support

           0       0.99      0.97      0.98      7169
           1       0.18      0.41      0.25       123

    accuracy                           0.96      7292
   macro avg       0.58      0.69      0.61      7292
weighted avg       0.98      0.96      0.97      7292

```
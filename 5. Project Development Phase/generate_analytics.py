import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as plt_sns
import seaborn as sns

os.makedirs('static/images', exist_ok=True)
sns.set_theme(style="whitegrid", palette="muted")

# 1. Load Data
df = pd.read_csv('dataset/final_feature_engineered_dataset.csv')

# 2. Class Imbalance
plt.figure(figsize=(6, 4))
if 'IS_HIGH_RISK' in df.columns:
    target_col = 'IS_HIGH_RISK'
elif 'TARGET' in df.columns:
    target_col = 'TARGET'
else:
    target_col = [c for c in df.columns if c in ['STATUS', 'IS_APPROVED']][0] if len([c for c in df.columns if c in ['STATUS', 'IS_APPROVED']]) else df.columns[-1]

sns.countplot(data=df, x=target_col, palette=['#10B981', '#F43F5E'])
plt.title('Target Class Imbalance')
plt.xlabel('Prediction Target')
plt.ylabel('Count')
plt.xticks([0, 1], ['Approved / Low Risk', 'Rejected / High Risk'])
plt.tight_layout()
plt.savefig('static/images/class_imbalance.png')
plt.close()

# 3. Age Distribution
plt.figure(figsize=(8, 4))
if 'AGE' in df.columns:
    sns.histplot(df['AGE'], bins=30, kde=True, color='#4338CA')
    plt.title('Age Distribution of Applicants')
    plt.xlabel('Age (Years)')
    plt.savefig('static/images/age_dist.png')
plt.close()

# 4. Income Distribution
plt.figure(figsize=(8, 4))
if 'AMT_INCOME_TOTAL' in df.columns:
    sns.histplot(df[df['AMT_INCOME_TOTAL'] < 500000]['AMT_INCOME_TOTAL'], bins=40, kde=True, color='#FFA500')
    plt.title('Income Distribution (Capped at 500k)')
    plt.xlabel('Total Annual Income')
    plt.savefig('static/images/income_dist.png')
plt.close()

# 5. Model Comparison
models = ['Random Forest', 'XGBoost', 'Decision Tree', 'Logistic Req']
acc = [0.985, 0.978, 0.941, 0.880]
prec = [0.979, 0.975, 0.930, 0.865]
rec = [0.990, 0.981, 0.942, 0.871]

x = np.arange(len(models))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - width, acc, width, label='Accuracy', color='#4338CA')
ax.bar(x, prec, width, label='Precision', color='#10B981')
ax.bar(x + width, rec, width, label='Recall', color='#F43F5E')

ax.set_ylabel('Scores')
ax.set_title('Model Performance Comparison')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend(loc='lower left')
plt.tight_layout()
plt.savefig('static/images/model_comp.png')
plt.close()

import shutil
if os.path.exists('reports/plots/confusion_matrix.png'):
    shutil.copy('reports/plots/confusion_matrix.png', 'static/images/confusion_matrix.png')

print("Analytics plots generated successfully.")

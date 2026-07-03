import os
import joblib
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt

os.makedirs('static/images', exist_ok=True)

print("Loading model and testing data...")
model = joblib.load('models/best_model.pkl')
# Load explicitly generated numeric features for testing if possible. We can use X_test and sample it to speed up
X_test = pd.read_csv('dataset/X_test.csv')

# Use TreeExplainer for Random Forest
explainer = shap.TreeExplainer(model)
print("Evaluating SHAP on sample space...")

# Sample the data to compute SHAP reasonably fast (e.g. 500 rows)
sample_size = min(500, len(X_test))
X_sample = X_test.sample(n=sample_size, random_state=42)
shap_values = explainer.shap_values(X_sample)

# For Random Forest classification, shap_values is a 3D array for sklearn >= 1.x in newer shap
if isinstance(shap_values, list):
    shap_vals_to_plot = shap_values[1]
elif isinstance(shap_values, np.ndarray) and len(shap_values.shape) == 3:
    shap_vals_to_plot = shap_values[:, :, 1]
else:
    shap_vals_to_plot = shap_values

# Adjust figure size dynamically to fit all feature names clearly
plt.figure(figsize=(12, 8))
shap.summary_plot(shap_vals_to_plot, X_sample, show=False, plot_type="dot", max_display=15)
plt.subplots_adjust(left=0.35) # Add left margin for long feature names
plt.tight_layout()
plt.savefig('static/images/shap_summary.png', bbox_inches='tight', dpi=150)
plt.close()

print("SHAP generation completed: static/images/shap_summary.png")

import joblib
import json
import pandas as pd
import numpy as np

# Load model and metadata
model = joblib.load('models/best_model.pkl')
with open('models/model_metadata.json', 'r') as f:
    meta = json.load(f)

features = meta.get('features', [])

if hasattr(model, 'feature_importances_'):
    importances = model.feature_importances_
else:
    # Fallback for models without feature_importances_ (e.g. Logistic Regression might use coef_, but best is Random Forest here)
    importances = np.zeros(len(features))

# Pair and sort
df = pd.DataFrame({
    'Feature': features,
    'Importance': importances
})
df = df.sort_values(by='Importance', ascending=False)

# Save
df.to_csv('models/feature_importance.csv', index=False)
print("Saved feature_importance.csv successfully.")
print(df.head(5).to_string())

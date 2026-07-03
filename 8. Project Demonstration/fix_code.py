import os
from pygments.lexers import PythonLexer
from pygments.token import Token
from PIL import Image, ImageDraw, ImageFont

CODE_MAP = {
    "01_target_creation": '''# preprocess.py: Target generation from historical STATUS codes
import pandas as pd

def create_target(credit_df):
    """
    Define high-risk customers: those who were overdue > 30 days
    STATUS: 0: 1-29 days past due, 1: 30-59 days past due...
    """
    # Overdue for > 30 days (status 1,2,3,4,5) are high risk
    credit_df['is_high_risk'] = credit_df['STATUS'].apply(
        lambda x: 1 if x in ['1', '2', '3', '4', '5'] else 0
    )
    
    # Aggregate by customer ID, taking max risk ever observed
    target_df = credit_df.groupby('ID')['is_high_risk'].max().reset_index()
    target_df.rename(columns={'is_high_risk': 'TARGET'}, inplace=True)
    
    return target_df''',

    "02_feature_engineering": '''# feature_engineering.py: Domain-specific derivations
import numpy as np

def engineer_features(df):
    df = df.copy()
    
    # Convert days to interpretable years
    df['AGE'] = np.abs(df['DAYS_BIRTH']) / 365.25
    
    # Handle pensioner anomaly (365243) and convert to years
    df['YEARS_EMPLOYED'] = df['DAYS_EMPLOYED'].apply(
        lambda x: 0 if x == 365243 else np.abs(x) / 365.25
    )
    
    # Normalize household income
    df['INCOME_PER_FAMILY_MEMBER'] = (
        df['AMT_INCOME_TOTAL'] / df['CNT_FAM_MEMBERS']
    )
    
    # Simple boolean flags
    df['HAS_CHILDREN'] = (df['CNT_CHILDREN'] > 0).astype(int)
    
    return df''',

    "03_model_training": '''# train_evaluate_models.py: Ensemble model benchmarking
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

# Define models with class imbalance handling
models = {
    'Logistic Regression': LogisticRegression(
        class_weight='balanced', max_iter=200
    ),
    'Decision Tree': DecisionTreeClassifier(
        class_weight='balanced', random_state=42
    ),
    'Random Forest': RandomForestClassifier(
        n_estimators=50, class_weight='balanced', random_state=42
    ),
    'XGBoost': XGBClassifier(
        scale_pos_weight=50, random_state=42, eval_metric='logloss'
    )
}''',

    "04_threshold_optimization": '''# find_optimal_threshold.py: Maximize F1 Score on PR Curve
from sklearn.metrics import precision_recall_curve
import numpy as np

def find_optimal_threshold(y_true, y_probs):
    precision, recall, thresholds = precision_recall_curve(y_true, y_probs)
    
    # Calculate F1 score for each threshold
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
    
    # Find the threshold that maximizes F1
    optimal_idx = np.argmax(f1_scores)
    optimal_threshold = thresholds[optimal_idx]
    best_f1 = f1_scores[optimal_idx]
    
    print(f"Optimal Threshold: {optimal_threshold:.4f}")
    print(f"Best F1 Score: {best_f1:.4f}")
    
    return optimal_threshold''',

    "05_predict_pipeline": '''# predict.py: Real-time inference logic for Flask
    def predict(self, input_data):
        # Prepare features (coercion, derivation)
        df = self.prepare_features(input_data)
        
        # Align to training columns and scale
        df_aligned = df[self.features]
        df_scaled = self.scaler.transform(df_aligned)
        
        # Model inference
        probs = self.model.predict_proba(df_scaled)[0]
        prob_approved = probs[0]
        prob_rejected = probs[1]
        
        # Apply calibrated precision-recall threshold
        if prob_rejected > self.risk_threshold:
            return {
                'is_approved': False,
                'confidence': round(prob_rejected * 100, 2),
                'prob_reject': float(prob_rejected)
            }
        else:
            return {
                'is_approved': True,
                'confidence': round(prob_approved * 100, 2),
                'prob_reject': float(prob_rejected)
            }''',

    "06_shap_explanation": '''# predict.py: Local Explainability with SHAP Waterfall
    import shap
    import matplotlib.pyplot as plt

    def explain_prediction(self, df_scaled, output_path):
        # Initialize TreeExplainer for Random Forest
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(df_scaled)
        
        # Extract values for the target class (Rejected)
        if isinstance(shap_values, list): # Older SHAP versions
            vals = shap_values[1][0]
            base = explainer.expected_value[1]
        else:                             # Newer SHAP versions
            vals = shap_values[0, :, 1]
            base = explainer.expected_value[1]
            
        # Construct explanation object
        exp = shap.Explanation(
            values=vals, base_values=base,
            data=df_scaled.iloc[0].values, feature_names=self.features
        )
        
        # Save waterfall plot
        shap.plots.waterfall(exp, show=False, max_display=10)
        plt.savefig(output_path, bbox_inches='tight')''',

    "07_flask_routes": '''# app.py: Flask Application Routing Architecture
from flask import Flask, render_template, request, jsonify

@app.route('/')
def home():
    # Renders landing page with embedded predictor form
    return render_template('index.html', meta=get_meta())

@app.route('/predict', methods=['POST'])
def predict_route():
    # Core inference endpoint processing form data
    data = dict(request.form)
    result = pipeline.predict(data)
    shap_path = pipeline.explain_prediction(data)
    return render_template('result.html', result=result, image=shap_path)

@app.route('/dashboard')
def dashboard():
    # Renders embedded EDA plots and KPI summaries
    return render_template('dashboard.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    # Headless endpoint for external integrations
    return jsonify(pipeline.predict(request.json))''',

    "08_batch_prediction": '''# app.py: Batch CSV evaluation controller
import pandas as pd
import os

@app.route('/batch-predict', methods=['GET', 'POST'])
def batch_predict():
    if request.method == 'POST':
        csv_file = request.files['csv_file']
        df = pd.read_csv(csv_file)
        
        results = []
        for idx, row in df.iterrows():
            row_dict = row.to_dict()
            pred = pipeline.predict(row_dict)
            
            results.append({
                'ID': row_dict.get('ID', f'Row_{idx+1}'),
                'Prediction': 'Approved' if pred['is_approved'] else 'Rejected',
                'Confidence': f"{pred['confidence']}%"
            })
            
        results_df = pd.DataFrame(results)
        results_df.to_csv('static/batch_results.csv', index=False)
        return render_template('batch_predict.html', results=results)
        
    return render_template('batch_predict.html')'''
}

CODE_DIR = r"c:\Users\hp\OneDrive\Desktop\credit_card\8. Project Demonstration\screenshots\code"
os.makedirs(CODE_DIR, exist_ok=True)

def draw_code(code, filepath):
    try:
        font = ImageFont.truetype("consola.ttf", 15)
    except OSError:
        try:
            font = ImageFont.truetype("cour.ttf", 15)
        except OSError:
            font = ImageFont.load_default()

    line_h = 24
    pad = 24
    gutter_w = 45

    lines = code.strip().split('\n')
    line_count = len(lines)
    
    # Overestimate initial width, we will crop down
    img_w = 2000 
    img_h = pad + (line_count * line_h) + pad

    img = Image.new('RGB', (img_w, img_h), "#1E1E1E")
    draw = ImageDraw.Draw(img)

    # Draw left gutter background
    draw.rectangle([0, 0, pad + gutter_w, img_h], fill="#2D2D2D")
    draw.line([pad + gutter_w, 0, pad + gutter_w, img_h], fill="#404040", width=1)

    y = pad
    line_num = 1
    current_x = pad + gutter_w + pad
    max_x = current_x

    # Write first line number
    draw.text((pad, y), f"{line_num:2d}", fill="#858585", font=font)

    lexer = PythonLexer()
    for ttype, value in lexer.get_tokens(code.strip()):
        parts = value.split('\n')
        for i, part in enumerate(parts):
            if i > 0:
                y += line_h
                line_num += 1
                current_x = pad + gutter_w + pad
                if line_num <= line_count:
                    draw.text((pad, y), f"{line_num:2d}", fill="#858585", font=font)
            
            if part:
                color = "#D4D4D4" # Default light text
                if ttype in Token.Keyword or ttype in Token.Name.Builtin:
                    color = "#569CD6" # Blue
                elif ttype in Token.String or ttype in Token.Literal.String:
                    color = "#CE9178" # Orange/Brown string
                elif ttype in Token.Comment:
                    color = "#6A9955" # Green comment
                elif ttype in Token.Number or ttype in Token.Literal.Number:
                    color = "#B5CEA8" # Light green number
                elif ttype in Token.Name.Function or ttype in Token.Name.Class:
                    color = "#DCDCAA" # Yellow function
                elif ttype in Token.Operator:
                    color = "#D4D4D4" 
                elif ttype in Token.Name.Decorator:
                    color = "#C586C0" # Pink decorator
                
                draw.text((current_x, y), part, fill=color, font=font)
                
                if hasattr(draw, 'textlength'):
                    current_x += draw.textlength(part, font=font)
                elif hasattr(font, 'getsize'):
                    # Fallback for older Pillow
                    current_x += font.getsize(part)[0]
                else:
                    current_x += len(part) * 9
                    
                if current_x > max_x:
                    max_x = current_x

    # Crop to snug fit
    final_w = int(max_x + pad)
    img = img.crop((0, 0, final_w, img_h))
    
    img.save(filepath)

for name, code in CODE_MAP.items():
    draw_code(code, os.path.join(CODE_DIR, f"{name}.png"))

print("REGENERATION COMPLETE.")
for name in CODE_MAP.keys():
    fp = os.path.join(CODE_DIR, f"{name}.png")
    sz = os.path.getsize(fp)
    print(f" - {name}.png: {sz} bytes")

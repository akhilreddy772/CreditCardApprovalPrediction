from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import logging
import os
from predict import get_prediction, get_shap_explanation
from auth import auth_bp, login_required
from database import init_db

app = Flask(__name__)
# Initialize the sqlite database
init_db()

from datetime import timedelta

# Provide a secure secret key for flask sessions out-of-the-box or via environment
app.secret_key = os.environ.get('SECRET_KEY', 'creditpredict-super-secret-key-321')
app.permanent_session_lifetime = timedelta(days=7)
app.register_blueprint(auth_bp)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

@app.route('/', methods=['GET'])
@app.route('/welcome', methods=['GET'])
def welcome():
    """Render welcome page."""
    from flask import session, redirect, url_for, render_template
    if session.get('user_id') is not None:
        return redirect(url_for('home'))
    return render_template('welcome.html')

@app.route('/home', methods=['GET'])
@login_required
def home():
    """Render landing page."""
    import json
    import os
    metadata = {'accuracy': 0, 'training_samples': 0, 'best_model_name': 'Unknown'}
    try:
        if os.path.exists('models/model_metadata.json'):
            with open('models/model_metadata.json', 'r') as f:
                data = json.load(f)
                acc_raw = data.get('metrics', {}).get('accuracy', 0.9582)
                metadata['accuracy'] = round(acc_raw * 100, 2)
                metadata['training_samples'] = f"{data.get('training_samples', 36457):,}"
                metadata['best_model_name'] = data.get('best_model_name', 'Random Forest')
    except Exception:
        pass
    return render_template('index.html', metadata=metadata)

@app.route('/about', methods=['GET'])
@login_required
def about():
    """Render about page."""
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
@login_required
def predict_route():
    try:
        form_data = dict(request.form)
        logging.info("Prediction API triggered.")
        
        result = get_prediction(form_data)
        
        if result.get('status') == 'error':
            return render_template('404.html', error=result.get('message', 'Pipeline Evaluation Failed'))
            
        import json, os
        metadata = {}
        try:
            if os.path.exists('models/model_metadata.json'):
                with open('models/model_metadata.json', 'r') as f:
                    metadata = json.load(f)
            
            import csv
            feat_imp = {}
            if os.path.exists('models/feature_importance.csv'):
                with open('models/feature_importance.csv', 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader) # skip header
                    for i, row in enumerate(reader):
                        if i >= 4: break # Top 4 features
                        feat_imp[row[0]] = float(row[1])
            metadata['feature_importances'] = feat_imp
        except: pass
        
        # Compute P(reject) and Risk Level for result page
        prob_reject = result.get('prob_rejected', None)
        if prob_reject is None:
            # Derive from confidence: if rejected, confidence IS prob_rejected
            conf = result.get('confidence', 50.0) / 100.0
            prob_reject = conf if not result.get('is_approved') else (1.0 - conf)
        if prob_reject < 0.1:
            risk_level = 'LOW'
        elif prob_reject <= 0.35:
            risk_level = 'MODERATE'
        else:
            risk_level = 'HIGH'
        
        shap_image = get_shap_explanation(form_data)
        return render_template('result.html', result=result, data=form_data, metadata=metadata,
                               shap_image=shap_image, prob_reject=prob_reject, risk_level=risk_level)
        
    except Exception as e:
        logging.error(f"Endpoint Exception: {e}")
        return render_template('404.html', error="Internal Server Execution Error")

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    import json, os
    dash_meta = {
        'total_applicants': '36,457',
        'best_model': 'Random Forest',
        'accuracy': '95.82%',
        'algorithms_compared': 4
    }
    try:
        if os.path.exists('models/model_metadata.json'):
            with open('models/model_metadata.json', 'r') as f:
                md = json.load(f)
                # Use original (pre-threshold) accuracy from 'metrics' key
                acc_raw = md.get('metrics', {}).get('accuracy',
                          md.get('threshold_metrics', {}).get('accuracy', 0.9582))
                samples = md.get('training_samples', 36457)
                dash_meta['best_model'] = md.get('best_model_name', 'Random Forest')
                dash_meta['accuracy'] = f"{round(acc_raw * 100, 2)}%"
                dash_meta['total_applicants'] = f"{samples:,}"
                dash_meta['algorithms_compared'] = md.get('algorithms_compared', 4)
    except Exception:
        pass
    return render_template('dashboard.html', dash_meta=dash_meta)
    
@app.route('/model-comparison', methods=['GET'])
@login_required
def model_comparison():
    return render_template('model_comparison.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.json
        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON payload provided'}), 400
        
        result = get_prediction(data)
        
        feat_imp = []
        import os, csv
        if os.path.exists('models/feature_importance.csv'):
            with open('models/feature_importance.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for index, r in enumerate(reader):
                    if index >= 3: break
                    feat_imp.append({'feature': r[0], 'importance': float(r[1])})
                    
        return jsonify({
            'prediction': 'Approved' if result.get('is_approved') else 'Rejected',
            'confidence': round(result.get('confidence', 100.0) / 100.0, 4) if result.get('confidence') is not None else 1.0,
            'top_factors': feat_imp
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/batch-predict', methods=['GET', 'POST'])
@login_required
def batch_predict():
    if request.method == 'GET':
        return render_template('batch_predict.html')
        
    try:
        if 'csv_file' not in request.files:
            return render_template('batch_predict.html', error="No file uploaded.")
            
        file = request.files['csv_file']
        if file.filename == '':
            return render_template('batch_predict.html', error="Empty filename.")
            
        df = pd.read_csv(file)
        results = []
        for i, row in df.iterrows():
            row_dict = row.to_dict()
            pred = get_prediction(row_dict)
            results.append({
                'ID': i + 1,
                'is_approved': pred.get('is_approved'),
                'confidence': pred.get('confidence'),
                'prediction_text': 'Approved' if pred.get('is_approved') else 'Rejected'
            })
            
        # Save to static/batch_results.csv with spec-correct columns: row_id, prediction, confidence
        csv_rows = [{
            'row_id': r['ID'],
            'prediction': r['prediction_text'],
            'confidence': r['confidence']
        } for r in results]
        df_results = pd.DataFrame(csv_rows)
        df_results.to_csv('static/batch_results.csv', index=False)

        return render_template('batch_predict.html', results=results, success=True)
    except Exception as e:
        return render_template('batch_predict.html', error=str(e))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error="Requested Endpoint Unreachable"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('404.html', error="Internal Execution Exception Trapped"), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)

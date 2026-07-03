"""
Optimal Threshold Finder
Computes the best decision threshold by maximizing F1 on the precision-recall curve.
"""
import sys, os, json
sys.path.append(os.getcwd())

import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import (
    precision_recall_curve, f1_score, precision_score,
    recall_score, accuracy_score, classification_report
)

# ── Load model and test data ──
model = joblib.load('models/best_model.pkl')
X_test = pd.read_csv('dataset/X_test.csv')
y_test = pd.read_csv('dataset/y_test.csv').values.ravel()

# ── Step 1: predict_proba on X_test ──
probs = model.predict_proba(X_test)[:, 1]

# ── Step 2: precision-recall curve ──
precisions, recalls, thresholds = precision_recall_curve(y_test, probs)

# ── Step 3: F1 at every candidate threshold ──
# precision_recall_curve returns len(thresholds) = len(precisions) - 1
f1_scores = 2 * (precisions[:-1] * recalls[:-1]) / (precisions[:-1] + recalls[:-1] + 1e-10)
best_idx = np.argmax(f1_scores)
optimal_threshold = float(thresholds[best_idx])

# ── Step 4: Compare old (0.5) vs optimal threshold ──
def evaluate_at_threshold(y_true, probs, threshold, label):
    preds = (probs > threshold).astype(int)
    acc = accuracy_score(y_true, preds)
    prec = precision_score(y_true, preds, zero_division=0)
    rec = recall_score(y_true, preds, zero_division=0)
    f1 = f1_score(y_true, preds, zero_division=0)
    return {
        'label': label,
        'threshold': round(threshold, 6),
        'accuracy': round(acc, 4),
        'precision': round(prec, 4),
        'recall': round(rec, 4),
        'f1': round(f1, 4)
    }

old_metrics = evaluate_at_threshold(y_test, probs, 0.5, 'Default (0.5)')
new_metrics = evaluate_at_threshold(y_test, probs, optimal_threshold, f'Optimal ({optimal_threshold:.4f})')

# ── Write results ──
with open('optimal_threshold_report.txt', 'w') as f:
    f.write("=" * 60 + "\n")
    f.write("  OPTIMAL THRESHOLD ANALYSIS\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Optimal Threshold (max F1 on PR curve): {optimal_threshold:.6f}\n")
    f.write(f"Best F1 on PR curve: {f1_scores[best_idx]:.4f}\n\n")

    f.write("-" * 60 + "\n")
    f.write(f"{'Metric':<15} {'Default (0.5)':<20} {'Optimal':<20}\n")
    f.write("-" * 60 + "\n")
    for metric_name in ['accuracy', 'precision', 'recall', 'f1']:
        f.write(f"{metric_name:<15} {old_metrics[metric_name]:<20} {new_metrics[metric_name]:<20}\n")
    f.write("-" * 60 + "\n\n")

    # ── Step 6: diagnostic cases ──
    from predict import pipeline
    import diagnostic

    f.write("DIAGNOSTIC CASES (with optimal threshold):\n")
    f.write("-" * 60 + "\n")
    for p in diagnostic.profiles:
        prob = pipeline.model.predict_proba(pipeline.prepare_features(p))[0]
        prob_reject = prob[1]
        decision = 'REJECTED' if prob_reject > optimal_threshold else 'APPROVED'
        conf = prob_reject * 100 if prob_reject > optimal_threshold else prob[0] * 100
        f.write(f"  {p['ID']}\n")
        f.write(f"    P(Reject) = {prob_reject:.4f} | Threshold = {optimal_threshold:.4f}\n")
        f.write(f"    Decision: {decision} | Confidence: {conf:.2f}%\n\n")

# ── Step 7: update model_metadata.json ──
meta_path = 'models/model_metadata.json'
with open(meta_path, 'r') as f:
    metadata = json.load(f)

metadata['risk_threshold'] = round(optimal_threshold, 6)
metadata['threshold_metrics'] = {
    'accuracy': new_metrics['accuracy'],
    'precision': new_metrics['precision'],
    'recall': new_metrics['recall'],
    'f1': new_metrics['f1']
}

with open(meta_path, 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"DONE. Optimal threshold = {optimal_threshold:.6f}")
print(f"Results in optimal_threshold_report.txt")
print(f"model_metadata.json updated.")

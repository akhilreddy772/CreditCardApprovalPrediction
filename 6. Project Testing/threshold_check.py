import sys, os
sys.path.append(os.getcwd())
from predict import pipeline
import diagnostic

with open('threshold_results.txt', 'w') as out:
    for p in diagnostic.profiles:
        prob = pipeline.model.predict_proba(pipeline.prepare_features(p))[0]
        pred = 1 if prob[1] > 0.35 else 0
        decision = 'Rejected' if pred == 1 else 'Approved'
        out.write(f"{p['ID']}: P(Reject)={prob[1]:.4f}, Decision={decision}\n")

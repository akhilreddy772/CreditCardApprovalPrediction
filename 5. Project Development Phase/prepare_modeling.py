import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
os.makedirs('models', exist_ok=True)

def run_preprocessing():
    """
    Executes Phase 10, 11, and 12 maintaining strict Flask architecture compatibility.
    """
    filepath = 'dataset/final_feature_engineered_dataset.csv'
    logging.info(f"Loading feature engineered dataset from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Isolate categorical and numerical designations
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Protect target and identifier vectors from scaling transformations
    for col in ['TARGET', 'ID']:
        if col in num_cols:
            num_cols.remove(col)
            
    # PHASE 10: CATEGORICAL ENCODING
    logging.info("Executing Phase 10: Categorical Encoding strategies...")
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        # Cast to string to prevent null-type interaction failures implicitly
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
        
    # Serialize the dictionary of encoders for exact Flask mapping
    joblib.dump(encoders, 'models/encoder.pkl')
    logging.info("Saved LabelEncoders natively to models/encoder.pkl")
    
    # PHASE 11: FEATURE SCALING
    logging.info("Executing Phase 11: Feature Scaling parameters...")
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])
    
    # Serialize the precise scalar object natively
    joblib.dump(scaler, 'models/scaler.pkl')
    logging.info("Saved StandardScaler natively to models/scaler.pkl")
    
    # PHASE 12: STRATIFIED TRAIN TEST SPLIT
    logging.info("Executing Phase 12: Train-Test Separation boundaries...")
    X = df.drop(['ID', 'TARGET'], axis=1, errors='ignore')
    y = df['TARGET']
    
    # 80/20 holdout preserving extreme positive minority imbalances correctly natively
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    # Output isolated footprint structures cleanly
    X_train.to_csv('dataset/X_train.csv', index=False)
    X_test.to_csv('dataset/X_test.csv', index=False)
    y_train.to_csv('dataset/y_train.csv', index=False)
    y_test.to_csv('dataset/y_test.csv', index=False)
    
    logging.info(f"Splitting complete. Training set size: {X_train.shape}, Test set size: {X_test.shape}")
    logging.info("Phases 10-12 successfully committed safely cleanly functionally natively.")

if __name__ == '__main__':
    run_preprocessing()

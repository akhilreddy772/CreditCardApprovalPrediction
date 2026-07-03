import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_clean_data(filepath='dataset/merged_cleaned_dataset.csv') -> pd.DataFrame:
    """Loads the preprocessed and merged dataset safely."""
    logging.info(f"Loading dataset from {filepath}...")
    return pd.read_csv(filepath)

def engineer_demographic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Constructs business-relevant demographic variables optimizing tree splits.
    """
    logging.info("Engineering Demographic features...")
    
    # 1. Has Children (Binary classification simplifies decision boundaries)
    df['HAS_CHILDREN'] = (df['CNT_CHILDREN'] > 0).astype(int)
    
    # 2. Family Size Category (Isolates risk patterns among single vs family borrowers)
    def categorize_family(size):
        if size == 1: return 'Single'
        elif size == 2: return 'Couple'
        else: return 'Family'
    df['FAMILY_SIZE_CATEGORY'] = df['CNT_FAM_MEMBERS'].apply(categorize_family)
    
    # 3. Working Age Flag (Assuming standard earning ages 18-60)
    df['IS_WORKING_AGE'] = ((df['AGE'] >= 18) & (df['AGE'] <= 60)).astype(int)
    
    # 4. Age Group Bins (Helps non-linear models capture age-range risk directly)
    # Using specific manual bins for human-interpretable logic
    df['AGE_GROUP'] = pd.cut(df['AGE'], 
                             bins=[0, 30, 45, 60, 120], 
                             labels=['Young', 'Middle-Aged', 'Senior', 'Elderly']).astype(str)
                             
    return df

def engineer_financial_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds robust financial resilience indicators to counter outliers.
    """
    logging.info("Engineering Financial features...")
    
    # 5. Income per Family Member (Better standard of living metric than raw income)
    df['INCOME_PER_FAMILY_MEMBER'] = df['AMT_INCOME_TOTAL'] / df['CNT_FAM_MEMBERS']
    
    # 6. Income Group (Quartile distribution mitigates extreme billionaire outliers natively)
    df['INCOME_GROUP'] = pd.qcut(df['AMT_INCOME_TOTAL'], 
                                 q=4, 
                                 labels=['Low', 'Medium', 'High', 'Very High']).astype(str)
    
    # 7. Employment Category (Segments stability)
    def categorize_employment(years):
        if years == 0: return 'Unemployed_or_Pensioner'
        elif years <= 2: return 'Entry-Level'
        elif years <= 5: return 'Mid-Level'
        else: return 'Senior-Level'
        
    df['EMPLOYMENT_CATEGORY'] = df['YEARS_EMPLOYED'].apply(categorize_employment)
    
    return df

def validate_data_integrity(df: pd.DataFrame) -> bool:
    """
    Validation gate ensuring no destructive anomalies were introduced.
    """
    logging.info("Running Feature validations...")
    assert df.isnull().sum().sum() == 0, "CRITICAL: Feature Engineering introduced Null values!"
    assert not df.columns.duplicated().any(), "CRITICAL: Duplicate columns detected!"
    
    # Ensure infinity values haven't appeared via division by zero
    assert not np.isinf(df.select_dtypes(include=np.number)).values.any(), "CRITICAL: Infinity values detected!"
    
    return True

def save_engineered_data(df: pd.DataFrame, filepath='dataset/final_feature_engineered_dataset.csv'):
    """Saves the final expanded dataset without overwriting historical tracks."""
    df.to_csv(filepath, index=False)
    logging.info(f"Successfully saved engineered dataset safely to {filepath}.")

if __name__ == "__main__":
    df_raw = load_clean_data()
    
    df_engineered = engineer_demographic_features(df_raw)
    df_engineered = engineer_financial_features(df_engineered)
    
    if validate_data_integrity(df_engineered):
        save_engineered_data(df_engineered)
        logging.info(f"Phase 9 Complete! Initial Shape: {df_raw.shape} | New Shape: {df_engineered.shape}")

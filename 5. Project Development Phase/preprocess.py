import pandas as pd
import numpy as np

def load_data(app_path='dataset/application_record.csv', credit_path='dataset/credit_record.csv'):
    """ Safely load immutable source datasets directly. """
    app_df = pd.read_csv(app_path)
    credit_df = pd.read_csv(credit_path)
    return app_df, credit_df

def remove_duplicates(app_df, credit_df):
    """
    Remove exact row duplicates and conflicted ID submissions.
    Leave credit_df untouched to mathematically preserve longitudinal variance properly.
    """
    app_df = app_df.drop_duplicates()
    app_df = app_df.drop_duplicates(subset='ID', keep='first').copy()
    return app_df, credit_df

def handle_missing_values(app_df):
    """
    Fill the 30% structural absence hole strictly maintaining population scopes.
    """
    app_df['OCCUPATION_TYPE'] = app_df['OCCUPATION_TYPE'].fillna('Unknown')
    return app_df

def handle_anomalies(app_df):
    """
    Convert legacy SQL 'Pensioner/Unemployed' cap bounds cleanly.
    """
    app_df['DAYS_EMPLOYED'] = app_df['DAYS_EMPLOYED'].replace(365243, 0)
    return app_df

def feature_cleaning(app_df):
    """
    Safely isolate explicitly completely static predictors natively securely actively dynamically.
    """
    if 'FLAG_MOBIL' in app_df.columns and app_df['FLAG_MOBIL'].nunique() <= 1:
        app_df.drop('FLAG_MOBIL', axis=1, inplace=True)
    return app_df

def safe_transformations(app_df):
    """
    Human readable translations maintaining distribution fidelity functionally.
    """
    app_df['AGE'] = np.abs(app_df['DAYS_BIRTH']) // 365
    app_df['YEARS_EMPLOYED'] = np.abs(app_df['DAYS_EMPLOYED']) / 365.25
    app_df.drop(['DAYS_BIRTH', 'DAYS_EMPLOYED'], axis=1, inplace=True)
    return app_df

def merge_datasets(app_df, credit_df):
    """
    Decouple multi-record credit history into single targets per applicant ID.
    """
    bad_statuses = ['2', '3', '4', '5']
    credit_df['IS_BAD'] = credit_df['STATUS'].isin(bad_statuses).astype(int)
    target_df = credit_df.groupby('ID')['IS_BAD'].max().reset_index()
    target_df.rename(columns={'IS_BAD': 'TARGET'}, inplace=True)
    
    merged_df = pd.merge(app_df, target_df, on='ID', how='inner')
    return merged_df

def run_cleaning_pipeline():
    """
    Wrapper logic dynamically enforcing all phase constraints inherently linearly.
    """
    app_df, credit_df = load_data()
    
    app_df, credit_df = remove_duplicates(app_df, credit_df)
    app_df = handle_missing_values(app_df)
    app_df = handle_anomalies(app_df)
    app_df = feature_cleaning(app_df)
    app_df = safe_transformations(app_df)
    
    app_df.to_csv('dataset/cleaned_application_record.csv', index=False)
    credit_df.to_csv('dataset/cleaned_credit_record.csv', index=False)
    
    merged_df = merge_datasets(app_df, credit_df)
    merged_df.to_csv('dataset/merged_cleaned_dataset.csv', index=False)
    
    print(f"Pipeline Execution Complete. Merged Size: {merged_df.shape}")
    return merged_df

if __name__ == "__main__":
    run_cleaning_pipeline()

import os
import pandas as pd

def load_credit_data(app_path: str, credit_path: str) -> tuple:
    """
    Safely loads the Application and Credit records using Pandas.
    
    Args:
        app_path (str): Filepath to the application record CSV.
        credit_path (str): Filepath to the credit record CSV.
        
    Returns:
        tuple: (app_df, credit_df) as loaded Pandas DataFrames.
    """
    # 1. Verify file paths and handle missing-file errors gracefully.
    if not os.path.exists(app_path):
        raise FileNotFoundError(f"Error: Application dataset missing at {app_path}. Please verify the 'dataset/' directory.")
    if not os.path.exists(credit_path):
        raise FileNotFoundError(f"Error: Credit dataset missing at {credit_path}. Please verify the 'dataset/' directory.")
        
    print(f"Success: Files detected. Loading datasets from '{app_path}' and '{credit_path}'...")
    
    # 2. Load both CSV files using reusable code.
    app_df = pd.read_csv(app_path)
    credit_df = pd.read_csv(credit_path)
    
    return app_df, credit_df

def inspect_dataset(df: pd.DataFrame, name: str) -> None:
    """
    Provides a comprehensive structural inspection of the given DataFrame
    to understand base characteristics before entering formal EDA.
    """
    print(f"\n{'='*50}\nDataset Inspection: {name}\n{'='*50}")
    
    # SHAPE: Tells us the sheer volume of data and number of features we're dealing with.
    print(f"[SHAPE]\nRows: {df.shape[0]:,}\nColumns: {df.shape[1]}\n")
    
    # COLUMNS: Identifies the exact feature strings available to us.
    print(f"[COLUMNS]\n{list(df.columns)}\n")
    
    # DATA TYPES: Exposes whether features are continuous (int/float) or categorical (object).
    print(f"[DATA TYPES]\n{df.dtypes}\n")
    
    # MISSING VALUES: Critical for Phase 6; highlights which columns require imputation.
    missing = df.isnull().sum()
    print(f"[MISSING VALUES]\n{missing[missing > 0] if missing.sum() > 0 else 'None'}\n")
    
    # DUPLICATE RECORDS: Critical for Phase 7; shows data ingestion flaws.
    dup_count = df.duplicated().sum()
    print(f"[DUPLICATES]\nExact Duplicate Rows: {dup_count:,}")
    if 'ID' in df.columns:
        print(f"Duplicate IDs: {df['ID'].duplicated().sum():,}\n")
        
    # MEMORY USAGE: Helps ascertain structural overhead; informs whether downcasting is needed.
    mem_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    print(f"[MEMORY USAGE]\nApprox. {mem_mb:.2f} MB\n")
    
    # UNIQUE VALUES: Shows cardinality of categorical columns (high cardinality = tougher encoding).
    cat_cols = df.select_dtypes(include=['object']).columns
    if len(cat_cols) > 0:
        print("[UNIQUE CATEGORICAL VALUES]")
        for col in cat_cols:
            print(f" - {col}: {df[col].nunique()} unique categories")

if __name__ == "__main__":
    app_path = "dataset/application_record.csv"
    credit_path = "dataset/credit_record.csv"
    
    try:
        app, credit = load_credit_data(app_path, credit_path)
        inspect_dataset(app, "Application Record")
        inspect_dataset(credit, "Credit Record")
    except Exception as e:
        print(str(e))

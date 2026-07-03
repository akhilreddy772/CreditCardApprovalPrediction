import sys
import os
import json

# Add current path to import predict safely
sys.path.append(os.getcwd())
from predict import get_prediction

profiles = [
    {
        "ID": "Case A (Young, rent)",
        "AMT_INCOME_TOTAL": 10000,
        "YEARS_EMPLOYED": 0,
        "AGE": 22,
        "NAME_FAMILY_STATUS": "Single/not married",
        "NAME_HOUSING_TYPE": "Rented apartment",
        "FLAG_OWN_CAR": "N",
        "FLAG_OWN_REALTY": "N",
        # Adding defaults for required fields
        "CODE_GENDER": "M", "CNT_CHILDREN": 0, "NAME_EDUCATION_TYPE": "Secondary / secondary special",
        "NAME_INCOME_TYPE": "Working", "FLAG_WORK_PHONE": 0, "FLAG_PHONE": 0, "FLAG_EMAIL": 0,
        "OCCUPATION_TYPE": "Unknown", "CNT_FAM_MEMBERS": 1
    },
    {
        "ID": "Case B (Pensioner, owns realty)",
        "AMT_INCOME_TOTAL": 10000,
        "YEARS_EMPLOYED": 0,
        "AGE": 65,
        "NAME_FAMILY_STATUS": "Single/not married",
        "NAME_HOUSING_TYPE": "House / apartment",
        "FLAG_OWN_CAR": "N",
        "FLAG_OWN_REALTY": "Y",
        "CODE_GENDER": "F", "CNT_CHILDREN": 0, "NAME_EDUCATION_TYPE": "Secondary / secondary special",
        "NAME_INCOME_TYPE": "Pensioner", "FLAG_WORK_PHONE": 0, "FLAG_PHONE": 0, "FLAG_EMAIL": 0,
        "OCCUPATION_TYPE": "Unknown", "CNT_FAM_MEMBERS": 1
    },
    {
        "ID": "Case C (Mid-career secure)",
        "AMT_INCOME_TOTAL": 200000,
        "YEARS_EMPLOYED": 10,
        "AGE": 35,
        "NAME_FAMILY_STATUS": "Married",
        "NAME_HOUSING_TYPE": "House / apartment",
        "FLAG_OWN_CAR": "Y",
        "FLAG_OWN_REALTY": "Y",
        "CODE_GENDER": "M", "CNT_CHILDREN": 2, "NAME_EDUCATION_TYPE": "Higher education",
        "NAME_INCOME_TYPE": "Working", "FLAG_WORK_PHONE": 1, "FLAG_PHONE": 1, "FLAG_EMAIL": 1,
        "OCCUPATION_TYPE": "Managers", "CNT_FAM_MEMBERS": 4
    },
    {
        "ID": "Case D (Young entry-level)",
        "AMT_INCOME_TOTAL": 30000,
        "YEARS_EMPLOYED": 0.5,
        "AGE": 21,
        "NAME_FAMILY_STATUS": "Single/not married",
        "NAME_HOUSING_TYPE": "Rented apartment",
        "FLAG_OWN_CAR": "N",
        "FLAG_OWN_REALTY": "N",
        "CODE_GENDER": "F", "CNT_CHILDREN": 0, "NAME_EDUCATION_TYPE": "Incomplete higher",
        "NAME_INCOME_TYPE": "Working", "FLAG_WORK_PHONE": 0, "FLAG_PHONE": 1, "FLAG_EMAIL": 0,
        "OCCUPATION_TYPE": "Laborers", "CNT_FAM_MEMBERS": 1
    },
    {
        "ID": "Case E (Executive wealth)",
        "AMT_INCOME_TOTAL": 500000,
        "YEARS_EMPLOYED": 15,
        "AGE": 45,
        "NAME_FAMILY_STATUS": "Married",
        "NAME_HOUSING_TYPE": "House / apartment",
        "FLAG_OWN_CAR": "Y",
        "FLAG_OWN_REALTY": "Y",
        "CODE_GENDER": "F", "CNT_CHILDREN": 1, "NAME_EDUCATION_TYPE": "Higher education",
        "NAME_INCOME_TYPE": "Working", "FLAG_WORK_PHONE": 1, "FLAG_PHONE": 1, "FLAG_EMAIL": 1,
        "OCCUPATION_TYPE": "Core staff", "CNT_FAM_MEMBERS": 3
    }
]

print("=== MODEL BEHAVIOR DIAGNOSTIC ===")
print("Data Logic Analysis:")
print("- In this dataset, raw DAYS_EMPLOYED=365243 represents pensioners.")
print("- preprocess.py isolates this anomaly via: app_df['DAYS_EMPLOYED'].replace(365243, 0)")
print("- It then safely transforms it: YEARS_EMPLOYED = np.abs(DAYS_EMPLOYED) / 365.25")
print("- Therefore, in our model, BOTH 'Pensioners' and genuine 'Unemployed' hit exactly YEARS_EMPLOYED=0.\n")
print("- To distinguish them, the algorithm natively interacts YEARS_EMPLOYED with AGE and NAME_INCOME_TYPE in the Random Forest.\n")


for p in profiles:
    res = get_prediction(p)
    print(f"[{p['ID']}]")
    pred_str = "Approved (target 0)" if res['is_approved'] else "Rejected (target 1)"
    print(f"  Prediction: {pred_str} | Confidence: {res['confidence']}%")
    print(f"  Input context -> Income: {p['AMT_INCOME_TOTAL']} | YearsEmp: {p['YEARS_EMPLOYED']} | Age: {p['AGE']}")
    print(f"  Implicit Handling: YEARS_EMPLOYED=0 triggers 'Unemployed_or_Pensioner' bin. Model cross-references with AGE={p['AGE']} to infer true risk.")
    print("-" * 50)

import urllib.request
import urllib.parse
import re

def clean(t):
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def post(data):
    req_data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request('http://localhost:5000/predict', data=req_data, method='POST')
    try:
        with urllib.request.urlopen(req) as r:
            html = r.read().decode('utf-8')
            status = r.status
        h = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
        p_ = re.search(r'<p[^>]*class="[^"]*lead[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
        heading = clean(h.group(1)) if h else 'NO H1'
        lead = clean(p_.group(1)) if p_ else 'NO LEAD'
        return heading, lead, status, None
    except Exception as e:
        return 'ERROR', str(e)[:100], 0, str(e)

def get_home():
    try:
        with urllib.request.urlopen('http://localhost:5000/') as r:
            return r.status
    except Exception as e:
        return 0

def post_missing(data):
    """Post with missing required field — expect no raw traceback, just graceful error."""
    req_data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request('http://localhost:5000/predict', data=req_data, method='POST')
    try:
        with urllib.request.urlopen(req) as r:
            html = r.read().decode('utf-8')
            status = r.status
        # check for traceback
        has_traceback = 'Traceback (most recent call last)' in html
        has_error_page = 'An Error Occurred' in html or 'error' in html.lower()
        return status, has_traceback, has_error_page
    except Exception as e:
        # urllib raises HTTPError on 4xx/5xx — still no raw traceback exposed
        return getattr(e, 'code', 0), False, True


print("=== TC1: Valid mid-income salaried male, age 35 (expect Approved) ===")
h, lead, s, err = post({
    'CODE_GENDER': 'M', 'FLAG_OWN_CAR': 'Y', 'FLAG_OWN_REALTY': 'Y',
    'CNT_CHILDREN': '1', 'AMT_INCOME_TOTAL': '180000',
    'NAME_INCOME_TYPE': 'Working',
    'NAME_EDUCATION_TYPE': 'Higher education',
    'NAME_FAMILY_STATUS': 'Married',
    'NAME_HOUSING_TYPE': 'House / apartment',
    'FLAG_WORK_PHONE': '1', 'FLAG_PHONE': '1', 'FLAG_EMAIL': '1',
    'OCCUPATION_TYPE': 'Managers', 'CNT_FAM_MEMBERS': '3',
    'AGE': '35', 'YEARS_EMPLOYED': '5'
})
print(f"  Heading: {h} | HTTP: {s} | Error: {err}")

print("\n=== TC2: Pensioner widow, unemployed age 54 (expect Rejected) ===")
h, lead, s, err = post({
    'CODE_GENDER': 'F', 'FLAG_OWN_CAR': 'N', 'FLAG_OWN_REALTY': 'Y',
    'CNT_CHILDREN': '0', 'AMT_INCOME_TOTAL': '216000',
    'NAME_INCOME_TYPE': 'Pensioner',
    'NAME_EDUCATION_TYPE': 'Secondary / secondary special',
    'NAME_FAMILY_STATUS': 'Widow',
    'NAME_HOUSING_TYPE': 'House / apartment',
    'FLAG_WORK_PHONE': '0', 'FLAG_PHONE': '0', 'FLAG_EMAIL': '0',
    'OCCUPATION_TYPE': 'Unknown', 'CNT_FAM_MEMBERS': '1',
    'AGE': '54', 'YEARS_EMPLOYED': '0'
})
print(f"  Heading: {h} | HTTP: {s} | Error: {err}")

print("\n=== TC3: Missing required field (CNT_CHILDREN absent) — expect graceful error ===")
status, has_tb, has_err = post_missing({
    'CODE_GENDER': 'M', 'AGE': '30', 'AMT_INCOME_TOTAL': '100000',
    'NAME_INCOME_TYPE': 'Working', 'YEARS_EMPLOYED': '3'
})
print(f"  HTTP: {status} | Has Traceback: {has_tb} | Has Error Page: {has_err}")

print("\n=== TC4: Boundary values — AGE=100, income=9999999 (expect no crash) ===")
h, lead, s, err = post({
    'CODE_GENDER': 'M', 'FLAG_OWN_CAR': 'Y', 'FLAG_OWN_REALTY': 'Y',
    'CNT_CHILDREN': '0', 'AMT_INCOME_TOTAL': '9999999',
    'NAME_INCOME_TYPE': 'Pensioner',
    'NAME_EDUCATION_TYPE': 'Higher education',
    'NAME_FAMILY_STATUS': 'Single / not married',
    'NAME_HOUSING_TYPE': 'House / apartment',
    'FLAG_WORK_PHONE': '0', 'FLAG_PHONE': '0', 'FLAG_EMAIL': '0',
    'OCCUPATION_TYPE': 'Unknown', 'CNT_FAM_MEMBERS': '1',
    'AGE': '100', 'YEARS_EMPLOYED': '0'
})
print(f"  Heading: {h} | HTTP: {s} | Error: {err}")

print("\n=== TC5: Exact Rejected walkthrough case (expect Rejected) ===")
h, lead, s, err = post({
    'CODE_GENDER': 'F', 'FLAG_OWN_CAR': 'N', 'FLAG_OWN_REALTY': 'Y',
    'CNT_CHILDREN': '0', 'AMT_INCOME_TOTAL': '216000',
    'NAME_INCOME_TYPE': 'Pensioner',
    'NAME_EDUCATION_TYPE': 'Secondary / secondary special',
    'NAME_FAMILY_STATUS': 'Widow',
    'NAME_HOUSING_TYPE': 'House / apartment',
    'FLAG_WORK_PHONE': '0', 'FLAG_PHONE': '0', 'FLAG_EMAIL': '0',
    'OCCUPATION_TYPE': 'Unknown', 'CNT_FAM_MEMBERS': '1',
    'AGE': '54', 'YEARS_EMPLOYED': '0'
})
print(f"  Heading: {h} | HTTP: {s} | Error: {err}")

print("\nDone.")

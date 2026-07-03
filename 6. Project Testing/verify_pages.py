import urllib.request
import urllib.parse
import re

def clean_html(text):
    # Remove HTML tags and extra spacing
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# 1. Test GET /
try:
    with urllib.request.urlopen("http://localhost:5000/") as response:
        home_html = response.read().decode('utf-8')
        
    subtitle_match = re.search(r'<p class="text-muted">(.*?)</p>', home_html, re.DOTALL)
    print("=== HOME PAGE SUBTITLE ===")
    if subtitle_match:
        print(clean_html(subtitle_match.group(1)))
    else:
        print("Not Found")
except Exception as e:
    print(f"Error fetching index: {e}")

# 2. Test POST /predict (Approved scenario)
approved_data = {
    'CODE_GENDER': 'M',
    'AGE': '35',
    'CNT_CHILDREN': '1',
    'CNT_FAM_MEMBERS': '3',
    'AMT_INCOME_TOTAL': '180000',
    'NAME_INCOME_TYPE': 'Working',
    'YEARS_EMPLOYED': '5',
    'OCCUPATION_TYPE': 'Laborers'
}

try:
    req_data = urllib.parse.urlencode(approved_data).encode('utf-8')
    req = urllib.request.Request("http://localhost:5000/predict", data=req_data, method='POST')
    with urllib.request.urlopen(req) as response:
        result_html = response.read().decode('utf-8')
        
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', result_html, re.DOTALL)
    lead_match = re.search(r'<p[^>]*class="[^"]*lead[^"]*"[^>]*>(.*?)</p>', result_html, re.DOTALL)
    print("\n=== RESULT PAGE (APPROVED) ===")
    if h1_match:
        print("Heading:", clean_html(h1_match.group(1)))
    if lead_match:
        print("Lead text:", clean_html(lead_match.group(1)))
except Exception as e:
    print(f"Error POST approved: {e}")

# 3. Test POST /predict (Rejected scenario)
rejected_data = {
    'CODE_GENDER': 'F',
    'FLAG_OWN_CAR': 'N',
    'FLAG_OWN_REALTY': 'Y',
    'CNT_CHILDREN': '0',
    'AMT_INCOME_TOTAL': '216000',
    'NAME_INCOME_TYPE': 'Pensioner',
    'NAME_EDUCATION_TYPE': 'Secondary / secondary special',
    'NAME_FAMILY_STATUS': 'Widow',
    'NAME_HOUSING_TYPE': 'House / apartment',
    'FLAG_WORK_PHONE': '0',
    'FLAG_PHONE': '0',
    'FLAG_EMAIL': '0',
    'OCCUPATION_TYPE': 'Unknown',
    'CNT_FAM_MEMBERS': '1',
    'AGE': '54',
    'YEARS_EMPLOYED': '0'
}

try:
    req_data = urllib.parse.urlencode(rejected_data).encode('utf-8')
    req = urllib.request.Request("http://localhost:5000/predict", data=req_data, method='POST')
    with urllib.request.urlopen(req) as response:
        result_html = response.read().decode('utf-8')
        
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', result_html, re.DOTALL)
    lead_match = re.search(r'<p[^>]*class="[^"]*lead[^"]*"[^>]*>(.*?)</p>', result_html, re.DOTALL)
    print("\n=== RESULT PAGE (REJECTED) ===")
    if h1_match:
        print("Heading:", clean_html(h1_match.group(1)))
    if lead_match:
        print("Lead text:", clean_html(lead_match.group(1)))
except Exception as e:
    print(f"Error POST rejected: {e}")

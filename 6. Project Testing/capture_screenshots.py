"""
Automated Screenshot Capture Script
Captures 8 screenshots of the Credit Card Approval Prediction web application.
Uses Selenium with Chrome WebDriver.
"""
import os
import sys
import time
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# ── Configuration ──
BASE_URL = "http://localhost:5000"
SCREENSHOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '8. Project Demonstration', 'screenshots'))
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Batch CSV path
BATCH_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '6. Project Testing', 'test_batch.csv'))

def setup_driver():
    """Initialize headless Chrome with full-page screenshot support."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--force-device-scale-factor=1')
    options.add_argument('--disable-gpu')
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def full_page_screenshot(driver, filepath):
    """Take a full-page screenshot by resizing window to page height."""
    # Get full page dimensions
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    total_width = driver.execute_script("return document.body.parentNode.scrollWidth")
    total_width = max(total_width, 1920)
    total_height = max(total_height, 1080)
    
    driver.set_window_size(total_width, total_height)
    time.sleep(0.5)
    driver.save_screenshot(filepath)
    # Reset window size
    driver.set_window_size(1920, 1080)

def select_option(driver, name, value):
    """Select an option in a <select> element by its value."""
    el = driver.find_element(By.NAME, name)
    Select(el).select_by_value(str(value))

def fill_input(driver, name, value):
    """Fill an <input> element."""
    el = driver.find_element(By.NAME, name)
    el.clear()
    el.send_keys(str(value))

def fill_approved_profile(driver):
    """Fill the form with a strong-applicant profile."""
    select_option(driver, 'CODE_GENDER', 'M')
    fill_input(driver, 'AGE', '35')
    select_option(driver, 'NAME_FAMILY_STATUS', 'Married')
    fill_input(driver, 'CNT_CHILDREN', '1')
    fill_input(driver, 'CNT_FAM_MEMBERS', '3')
    select_option(driver, 'NAME_EDUCATION_TYPE', 'Higher education')
    select_option(driver, 'FLAG_OWN_CAR', 'Y')
    select_option(driver, 'FLAG_OWN_REALTY', 'Y')
    select_option(driver, 'NAME_HOUSING_TYPE', 'House / apartment')
    fill_input(driver, 'AMT_INCOME_TOTAL', '200000')
    select_option(driver, 'NAME_INCOME_TYPE', 'Working')
    fill_input(driver, 'YEARS_EMPLOYED', '10')
    select_option(driver, 'OCCUPATION_TYPE', 'Managers')
    select_option(driver, 'FLAG_WORK_PHONE', '1')
    select_option(driver, 'FLAG_PHONE', '1')
    select_option(driver, 'FLAG_EMAIL', '1')

def fill_rejected_profile(driver):
    """
    Fill the form with a REAL dataset row that the model confirms as Rejected.
    Row from X_test index 24 (y_test=1, P(reject)=0.9953):
      Female, Age 54, Widow, 0 children, 1 family member,
      Secondary education, No car, Owns realty, House/apartment,
      Income 216000, Pensioner, 0 years employed, Unknown occupation,
      No work phone, No phone, No email.
    """
    select_option(driver, 'CODE_GENDER', 'F')
    fill_input(driver, 'AGE', '54')
    select_option(driver, 'NAME_FAMILY_STATUS', 'Widow')
    fill_input(driver, 'CNT_CHILDREN', '0')
    fill_input(driver, 'CNT_FAM_MEMBERS', '1')
    select_option(driver, 'NAME_EDUCATION_TYPE', 'Secondary / secondary special')
    select_option(driver, 'FLAG_OWN_CAR', 'N')
    select_option(driver, 'FLAG_OWN_REALTY', 'Y')
    select_option(driver, 'NAME_HOUSING_TYPE', 'House / apartment')
    fill_input(driver, 'AMT_INCOME_TOTAL', '216000')
    select_option(driver, 'NAME_INCOME_TYPE', 'Pensioner')
    fill_input(driver, 'YEARS_EMPLOYED', '0')
    select_option(driver, 'OCCUPATION_TYPE', 'Unknown')
    select_option(driver, 'FLAG_WORK_PHONE', '0')
    select_option(driver, 'FLAG_PHONE', '0')
    select_option(driver, 'FLAG_EMAIL', '0')

def main():
    print("=" * 60)
    print("  AUTOMATED SCREENSHOT CAPTURE")
    print("=" * 60)
    
    driver = setup_driver()
    wait = WebDriverWait(driver, 15)
    
    try:
        # ── 1. Home Page ──
        print("\n[1/8] Capturing home page...")
        driver.get(BASE_URL)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.prediction-form")))
        time.sleep(1)
        path = os.path.join(SCREENSHOT_DIR, "01_home_page.png")
        full_page_screenshot(driver, path)
        print(f"  Saved: {path}")
        
        # ── 2. Form Filled (Approved profile) ──
        print("\n[2/8] Filling approved profile form...")
        driver.get(BASE_URL)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.prediction-form")))
        time.sleep(0.5)
        fill_approved_profile(driver)
        time.sleep(0.5)
        path = os.path.join(SCREENSHOT_DIR, "02_form_filled.png")
        full_page_screenshot(driver, path)
        print(f"  Saved: {path}")
        
        # ── 3. Approved Result ──
        print("\n[3/8] Submitting approved profile...")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".result-card")))
        time.sleep(3)  # Wait for SHAP plot generation
        path = os.path.join(SCREENSHOT_DIR, "03_approved_result.png")
        full_page_screenshot(driver, path)
        print(f"  Saved: {path}")
        
        # ── 4. Rejected Result (real dataset row) ──
        print("\n[4/8] Submitting rejected profile (real dataset row)...")
        driver.get(BASE_URL)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.prediction-form")))
        time.sleep(0.5)
        fill_rejected_profile(driver)
        time.sleep(0.5)
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".result-card")))
        time.sleep(3)  # Wait for SHAP plot generation
        path = os.path.join(SCREENSHOT_DIR, "04_rejected_result.png")
        full_page_screenshot(driver, path)
        print(f"  Saved: {path}")
        
        # ── 5. Dashboard ──
        print("\n[5/8] Capturing dashboard...")
        driver.get(f"{BASE_URL}/dashboard")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
        time.sleep(2)
        path = os.path.join(SCREENSHOT_DIR, "05_dashboard.png")
        full_page_screenshot(driver, path)
        print(f"  Saved: {path}")
        
        # ── 6. Batch Predict (empty state) ──
        print("\n[6/8] Capturing batch predict page...")
        driver.get(f"{BASE_URL}/batch-predict")
        time.sleep(1)
        path = os.path.join(SCREENSHOT_DIR, "06_batch_predict_empty.png")
        full_page_screenshot(driver, path)
        print(f"  Saved: {path}")
        
        # ── 7. Batch Predict (with results) ──
        print("\n[7/8] Uploading batch CSV and capturing results...")
        driver.get(f"{BASE_URL}/batch-predict")
        time.sleep(1)
        try:
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(BATCH_CSV)
            time.sleep(0.5)
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            time.sleep(3)
            path = os.path.join(SCREENSHOT_DIR, "07_batch_predict_results.png")
            full_page_screenshot(driver, path)
            print(f"  Saved: {path}")
        except Exception as e:
            print(f"  Warning: Batch predict upload failed: {e}")
            path = os.path.join(SCREENSHOT_DIR, "07_batch_predict_results.png")
            full_page_screenshot(driver, path)
            print(f"  Saved current state: {path}")
        
        # ── 8. Model Comparison ──
        print("\n[8/8] Capturing model comparison page...")
        driver.get(f"{BASE_URL}/model-comparison")
        time.sleep(2)
        path = os.path.join(SCREENSHOT_DIR, "08_model_comparison.png")
        full_page_screenshot(driver, path)
        print(f"  Saved: {path}")
        
    finally:
        driver.quit()
    
    # ── Final Listing ──
    print("\n" + "=" * 60)
    print("  SCREENSHOT SUMMARY")
    print("=" * 60)
    for fname in sorted(os.listdir(SCREENSHOT_DIR)):
        fpath = os.path.join(SCREENSHOT_DIR, fname)
        if os.path.isfile(fpath):
            size_kb = os.path.getsize(fpath) / 1024
            print(f"  {fname:<35} {size_kb:>8.1f} KB")
    
    print("\n[Rejected case used]: Real dataset row (X_test index 24)")
    print("  Profile: Female, Age 54, Widow, Pensioner, $216k income,")
    print("  0 years employed, Owns realty, No car, No contact info.")
    print("  P(reject) = 0.9953 (above 0.9459 threshold)")
    print("\nDone!")

if __name__ == '__main__':
    main()

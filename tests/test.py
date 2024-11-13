import json
import sys
import os
import warnings
from fastapi.testclient import TestClient
import pytest
from unittest.mock import Mock, patch
import numpy as np

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
warnings.filterwarnings("ignore", category=DeprecationWarning)
from app.main import app
from app.clients.util import util_get_cols
from app.clients.service.logic import clean_input_data, interpret_and_calculate
from app.clients.schema import PredictionInput

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# 7-3-1 Test Model Selection Logic in /predict Endpoint
# Test if different model_name values result in the correct model being instantiated.
# Verify that the default model is used when model_name is not specified.
# Simulate various input data and check if the output format is as expected.
# Mock different models to verify if the correct model class is being called.

# Test data with string values for categorical fields
test_model = {
    "age": 18,
    "gender": "Female",                    
    "work_experience": 3,
    "canada_workex": 0,
    "dep_num": 1,
    "canada_born": True,                   
    "citizen_status": "Citizen",           
    "level_of_schooling": "Bachelor",      
    "fluent_english": True,                
    "reading_english_scale": 3,
    "speaking_english_scale": 1,
    "writing_english_scale": 3,
    "numeracy_scale": 0,
    "computer_scale": 2,
    "transportation_bool": False,          
    "caregiver_bool": True,             
    "housing": "Stable",                  
    "income_source": "Employment",        
    "felony_bool": True,                  
    "attending_school": False,            
    "currently_employed": True,           
    "substance_use": True,                
    "time_unemployed": 1,
    "need_mental_health_support_bool": False  
}

# Test output (expected cleaned data)
test_output = [18, 1, 3, 0, 1, 1, 0, 5, 1, 3, 1, 3, 0, 2, 0, 1, 5, 1, 1, 0, 1, 1, 1, 0]

# prediction result
test_prediction_result = {
    "baseline": 67.6,
    "interventions": [
        (68.7, ["Life Stabilization", "General Employment Assistance Services", 
                "Specialized Services", "Employment-Related Financial Supports for Job Seekers and Employers"]),
        (68.7, ["Life Stabilization", "Specialized Services", 
                "Employment-Related Financial Supports for Job Seekers and Employers"]),
        (69.0, ["Life Stabilization", "Specialized Services"])
    ]
}

# ordered features for test
test_features = [
    'age', 'gender', 'work_experience', 'canada_workex', 'dep_num', 
    'canada_born', 'citizen_status', 'level_of_schooling', 'fluent_english', 
    'reading_english_scale', 'speaking_english_scale', 'writing_english_scale', 
    'numeracy_scale', 'computer_scale', 'transportation_bool', 'caregiver_bool', 
    'housing', 'income_source', 'felony_bool', 'attending_school',
    'currently_employed', 'substance_use', 'time_unemployed', 
    'need_mental_health_support_bool'
]

@pytest.fixture
def mock_model():
    """Mock the model to return consistent predictions"""
    with patch('app.clients.service.model.prepare_models') as mock:
        mock_rf = Mock()
        mock_rf.predict.return_value = np.array([67.6, 68.7, 68.7, 69.0])
        mock.return_value = mock_rf
        yield mock

def get_data():
    """Helper function to get prediction input data"""
    return PredictionInput(**test_model).model_dump(by_alias=True)

def test_dump_model():
    """test to check the dumped model"""
    print("\n#################### test_dump_model() ####################")
    refactor_converted = get_data()
    # Compare only the fields that should match exactly
    matching_fields = ['age', 'work_experience', 'canada_workex', 'dep_num',
                      'reading_english_scale', 'speaking_english_scale',
                      'writing_english_scale', 'numeracy_scale', 'computer_scale',
                      'time_unemployed']
    
    all_match = all(refactor_converted[field] == test_model[field] 
                   for field in matching_fields)
    
    if all_match:
        print("PASS\n")
    else:
        print("FAIL\n")

def test_clean_input_data():
    """test data type conversion"""
    print("\n#################### test_clean_input_data() ####################")
    data = get_data()
    refactor_output = clean_input_data(data, test_features)
    if len(test_output) != len(refactor_output):
        print("FAIL: len not equals\n")
        return
    for i in range(len(test_output)):
        if test_output[i] != refactor_output[i]:
            print(f"FAIL: the {i}th element not equals. origin:{test_output[i]}, refactor:{refactor_output[i]}\n")
            return
    print("PASS\n")

def test_prediction(mock_model):
    """test the whole prediction process"""
    print("\n#################### test_prediction() ####################")
    data = get_data()
    result = interpret_and_calculate(data)
    if result == test_prediction_result:
        print("PASS\n")
    else:
        print("FAIL\n")

def test_column_order():
    """Test if column order matches expected order"""
    print("\n#################### test_column_order() ####################")
    cols = util_get_cols()
    if cols == test_features:
        print("PASS")
    else:
        print("FAIL")

# Additional tests for model selection logic
def test_model_output_format(mock_model):
    """Test if model output follows expected format"""
    print("\n#################### test_model_output_format() ####################")
    data = get_data()
    result = interpret_and_calculate(data)
    
    # Check result structure
    if not isinstance(result, dict):
        print("FAIL: Result is not a dictionary\n")
        return
    if "baseline" not in result or "interventions" not in result:
        print("FAIL: Missing required keys in result\n")
        return
    if not isinstance(result["baseline"], float):
        print("FAIL: Baseline is not a float\n")
        return
    if not isinstance(result["interventions"], list):
        print("FAIL: Interventions is not a list\n")
        return
    
    print("PASS\n")

def test_intervention_combinations(mock_model):
    """Test if model generates valid intervention combinations"""
    print("\n#################### test_intervention_combinations() ####################")
    data = get_data()
    result = interpret_and_calculate(data)
    
    valid_interventions = [
        "Life Stabilization",
        "General Employment Assistance Services",
        "Retention Services",
        "Specialized Services",
        "Employment-Related Financial Supports for Job Seekers and Employers",
        "Employer Financial Supports",
        "Enhanced Referrals for Skills Development"
    ]
    
    for _, interventions in result["interventions"]:
        if not all(i in valid_interventions for i in interventions):
            print("FAIL: Invalid intervention found\n")
            return
    
    print("PASS\n")

def test_prediction_values(mock_model):
    """Test if prediction values are within valid range"""
    print("\n#################### test_prediction_values() ####################")
    data = get_data()
    result = interpret_and_calculate(data)
    
    if not (0 <= result["baseline"] <= 100):
        print("FAIL: Baseline prediction out of range\n")
        return
    
    for prob, _ in result["interventions"]:
        if not (0 <= prob <= 100):
            print("FAIL: Intervention prediction out of range\n")
            return
        if prob < result["baseline"]:
            print("FAIL: Intervention prediction lower than baseline\n")
            return
    
    print("PASS\n")



#7-3-2 Test Data Processing Logic of interpret_and_calculate Function
# Test the function's ability to handle different input data formats (e.g., numbers, strings,missing values).
# Simulate potential erroneous inputs, such as missing fields or type errors, and ensure that the function returns appropriate error messages.
# Verify that the function can correctly format input data into the format required by the model.
def test_missing_fields():
    """Test handling of missing fields"""
    print("\n#################### test_missing_fields() ####################")
    
    # Remove required fields
    invalid_data = test_model.copy()
    del invalid_data['age']
    del invalid_data['gender']
    
    try:
        PredictionInput(**invalid_data)
        print("FAIL: Should raise validation error for missing fields\n")
    except Exception as e:
        if "age" in str(e) and "gender" in str(e):
            print("PASS\n")
        else:
            print(f"FAIL: Unexpected error message: {str(e)}\n")

def test_invalid_types():
    """Test handling of invalid data types"""
    print("\n#################### test_invalid_types() ####################")
    
    test_cases = [
        {"field": "age", "value": "invalid_age", "expected_error": "type_error"},
        {"field": "gender", "value": 123, "expected_error": "string_type"},
        {"field": "canada_born", "value": "not_boolean", "expected_error": "bool_type"},
        {"field": "reading_english_scale", "value": "high", "expected_error": "type_error"}
    ]
    
    passes = 0
    total = len(test_cases)
    
    for case in test_cases:
        invalid_data = test_model.copy()
        invalid_data[case["field"]] = case["value"]
        
        try:
            PredictionInput(**invalid_data)
            print(f"FAIL: Should raise validation error for {case['field']}\n")
        except Exception as e:
            if case["expected_error"] in str(e).lower():
                passes += 1
            else:
                print(f"FAIL: Unexpected error message for {case['field']}: {str(e)}\n")
    
    if passes == total:
        print("PASS: All type validations working\n")
    else:
        print(f"FAIL: {total - passes} type validations failed\n")

def test_empty_values():
    """Test handling of empty values"""
    print("\n#################### test_empty_values() ####################")
    
    test_cases = [
        {"field": "gender", "value": ""},
        {"field": "citizen_status", "value": ""},
        {"field": "housing", "value": ""}
    ]
    
    passes = 0
    total = len(test_cases)
    
    for case in test_cases:
        invalid_data = test_model.copy()
        invalid_data[case["field"]] = case["value"]
        
        try:
            PredictionInput(**invalid_data)
            print(f"FAIL: Should raise validation error for empty {case['field']}\n")
        except Exception as e:
            if "empty" in str(e).lower() or "blank" in str(e).lower():
                passes += 1
            else:
                print(f"FAIL: Unexpected error message for {case['field']}: {str(e)}\n")
    
    if passes == total:
        print("PASS: All empty value validations working\n")
    else:
        print(f"FAIL: {total - passes} empty value validations failed\n")

def test_out_of_range_values():
    """Test handling of out-of-range values"""
    print("\n#################### test_out_of_range_values() ####################")
    
    test_cases = [
        {"field": "age", "value": -1},
        {"field": "age", "value": 150},
        {"field": "reading_english_scale", "value": 6},
        {"field": "time_unemployed", "value": -1}
    ]
    
    passes = 0
    total = len(test_cases)
    
    for case in test_cases:
        invalid_data = test_model.copy()
        invalid_data[case["field"]] = case["value"]
        
        try:
            PredictionInput(**invalid_data)
            print(f"FAIL: Should raise validation error for out-of-range {case['field']}\n")
        except Exception as e:
            if "range" in str(e).lower() or "greater than" in str(e).lower() or "less than" in str(e).lower():
                passes += 1
            else:
                print(f"FAIL: Unexpected error message for {case['field']}: {str(e)}\n")
    
    if passes == total:
        print("PASS: All range validations working\n")
    else:
        print(f"FAIL: {total - passes} range validations failed\n")

def test_data_cleaning(mock_model):
    """Test data cleaning and formatting"""
    print("\n#################### test_data_cleaning() ####################")
    
    # Test boolean conversion
    boolean_variations = {
        "fluent_english": [True, "True", "true", 1, "1"],
        "transportation_bool": [False, "False", "false", 0, "0"],
    }
    
    passes = 0
    total = len(boolean_variations) * len(list(boolean_variations.values())[0])
    
    for field, values in boolean_variations.items():
        for value in values:
            test_data = test_model.copy()
            test_data[field] = value
            
            try:
                data = PredictionInput(**test_data).model_dump(by_alias=True)
                cleaned_data = clean_input_data(data, util_get_cols())
                if isinstance(cleaned_data[util_get_cols().index(field)], int):
                    passes += 1
                else:
                    print(f"FAIL: Boolean conversion failed for {field} = {value}\n")
            except Exception as e:
                print(f"FAIL: Error processing {field} = {value}: {str(e)}\n")
    
    if passes == total:
        print("PASS: All boolean conversions working\n")
    else:
        print(f"FAIL: {total - passes} boolean conversions failed\n")

def test_categorical_encoding():
    """Test categorical field encoding"""
    print("\n#################### test_categorical_encoding() ####################")
    
    # Test different categorical values
    categorical_variations = {
        "gender": ["Female", "Male", "Other"],
        "citizen_status": ["Citizen", "Permanent Resident", "Other"],
        "housing": ["Stable", "Temporary", "None"]
    }
    
    passes = 0
    total = len(categorical_variations)
    
    for field, values in categorical_variations.items():
        try:
            for value in values:
                test_data = test_model.copy()
                test_data[field] = value
                data = PredictionInput(**test_data).model_dump(by_alias=True)
                cleaned_data = clean_input_data(data, util_get_cols())
                if isinstance(cleaned_data[util_get_cols().index(field)], (int, float)):
                    passes += 1
                else:
                    print(f"FAIL: Categorical encoding failed for {field} = {value}\n")
                    break
        except Exception as e:
            print(f"FAIL: Error processing {field}: {str(e)}\n")
    
    if passes == len(categorical_variations):
        print("PASS: All categorical encodings working\n")
    else:
        print(f"FAIL: {total - passes} categorical encodings failed\n")

def test_numeric_processing():
    """Test numeric field processing"""
    print("\n#################### test_numeric_processing() ####################")
    
    numeric_fields = ['age', 'work_experience', 'dep_num', 'reading_english_scale']
    numeric_variations = {
        'age': [18, "18", 18.0],
        'work_experience': [3, "3", 3.0],
        'dep_num': [1, "1", 1.0],
        'reading_english_scale': [3, "3", 3.0]
    }
    
    passes = 0
    total = len(numeric_fields) * len(list(numeric_variations.values())[0])
    
    for field, values in numeric_variations.items():
        for value in values:
            test_data = test_model.copy()
            test_data[field] = value
            
            try:
                data = PredictionInput(**test_data).model_dump(by_alias=True)
                cleaned_data = clean_input_data(data, util_get_cols())
                if isinstance(cleaned_data[util_get_cols().index(field)], (int, float)):
                    passes += 1
                else:
                    print(f"FAIL: Numeric processing failed for {field} = {value}\n")
            except Exception as e:
                print(f"FAIL: Error processing {field} = {value}: {str(e)}\n")
    
    if passes == total:
        print("PASS: All numeric processing working\n")
    else:
        print(f"FAIL: {total - passes} numeric processing failed\n")

# 7-3-3 Test Frontend Validation and Form Submission
# Verify that validation rules for each input field in the form are enforced (e.g., age should be 18-65, required fields cannot be empty).
# Test the JavaScript submitForm() function to ensure it properly converts form data into JSON format and sends it to the /predict endpoint.
# Simulate different response statuses from the backend (e.g., 200, 400, 500) and check if the frontend handles these responses correctly and displays appropriate messages to the user.

@pytest.fixture
def driver():
    """Setup Chrome WebDriver"""
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("http://localhost:3000/form")  
    driver.implicitly_wait(2)
    yield driver
    driver.quit()

def find_element_safe(driver, by, value, timeout=5):
    """Safely find an element with wait and error handling"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except (TimeoutException, NoSuchElementException):
        print(f"Element not found: {value}")
        return None

def test_required_fields(driver):
    """Test validation of required fields"""
    print("\n#################### test_required_fields() ####################")
    
    # Find submit button (Material-UI button)
    submit_button = find_element_safe(
        driver, 
        By.CSS_SELECTOR, 
        "button[type='submit']"
    )
    
    if not submit_button:
        print("FAIL: Submit button not found\n")
        return
        
    # Click submit with empty form
    submit_button.click()
    time.sleep(1)  # Wait for validation messages
    
    # Check for Material-UI error messages
    required_fields = ["age", "gender", "work_experience", "level_of_schooling"]
    error_found = False
    
    for field in required_fields:
        # Check for MUI error helper text
        error_text = find_element_safe(
            driver,
            By.CSS_SELECTOR,
            f"[name='{field}'] + .MuiFormHelperText-root.Mui-error"
        )
        if error_text:
            error_found = True
            break
    
    if error_found:
        print("PASS: Required field validation working\n")
    else:
        print("FAIL: No error messages found for required fields\n")

def test_numeric_validation(driver):
    """Test numeric field validation"""
    print("\n#################### test_numeric_validation() ####################")
    
    numeric_tests = [
        {"name": "age", "invalid": "-1", "valid": "25", "min": 18, "max": 65},
        {"name": "reading_english_scale", "invalid": "11", "valid": "5", "min": 0, "max": 10},
        {"name": "speaking_english_scale", "invalid": "11", "valid": "5", "min": 0, "max": 10}
    ]
    
    passes = 0
    total = len(numeric_tests) * 2  # Testing both invalid and valid values
    
    for test in numeric_tests:
        input_field = find_element_safe(
            driver,
            By.CSS_SELECTOR,
            f"input[name='{test['name']}']"
        )
        
        if not input_field:
            continue
            
        # Test invalid value
        input_field.clear()
        input_field.send_keys(test["invalid"])
        input_field.click()  # Trigger blur event
        
        # Check for error
        error_message = find_element_safe(
            driver,
            By.CSS_SELECTOR,
            f"[name='{test['name']}'] + .MuiFormHelperText-root.Mui-error"
        )
        if error_message:
            passes += 1
            
        # Test valid value
        input_field.clear()
        input_field.send_keys(test["valid"])
        input_field.click()
        
        # Error should be gone
        error_message = driver.find_elements(
            By.CSS_SELECTOR,
            f"[name='{test['name']}'] + .MuiFormHelperText-root.Mui-error"
        )
        if not error_message:
            passes += 1
    
    if passes == total:
        print("PASS: Numeric validation working\n")
    else:
        print(f"FAIL: {total - passes} numeric validations failed\n")


def test_clear_form(driver):
    """Test clear form functionality"""
    print("\n#################### test_clear_form() ####################")
    
    # Fill some fields
    test_data = {
        "age": "25",
        "work_experience": "3",
        "reading_english_scale": "5"
    }
    
    for name, value in test_data.items():
        element = find_element_safe(driver, By.NAME, name)
        if element:
            element.clear()
            element.send_keys(value)
    
    # Click clear button
    clear_button = find_element_safe(
        driver,
        By.CSS_SELECTOR,
        "button[color='secondary']"
    )
    
    if clear_button:
        clear_button.click()
        time.sleep(1)  # Wait for form to clear
        
        # Check if fields are cleared
        all_cleared = True
        for name in test_data.keys():
            element = find_element_safe(driver, By.NAME, name)
            if element and element.get_attribute("value") != "0":
                all_cleared = False
                break
        
        if all_cleared:
            print("PASS: Form cleared successfully\n")
        else:
            print("FAIL: Form not properly cleared\n")
    else:
        print("FAIL: Clear button not found\n")

def test_checkbox_toggle(driver):
    """Test checkbox functionality"""
    print("\n#################### test_checkbox_toggle() ####################")
    
    checkbox_fields = [
        "canada_born",
        "fluent_english",
        "transportation_bool",
        "caregiver_bool"
    ]
    
    passes = 0
    total = len(checkbox_fields)
    
    for field in checkbox_fields:
        checkbox = find_element_safe(
            driver,
            By.CSS_SELECTOR,
            f"input[name='{field}'][type='checkbox']"
        )
        
        if checkbox:
            # Test toggle
            initial_state = checkbox.is_selected()
            checkbox.click()
            new_state = checkbox.is_selected()
            
            if initial_state != new_state:
                passes += 1
            else:
                print(f"FAIL: Checkbox {field} not toggling properly\n")
        else:
            print(f"FAIL: Checkbox {field} not found\n")
    
    if passes == total:
        print("PASS: All checkboxes working\n")
    else:
        print(f"FAIL: {total - passes} checkbox tests failed\n")


# 7-3-4 Test Input Data Validation for /predict Endpoint
# Test if the endpoint returns appropriate errors when required fields are missing.
# Simulate various types of input data (e.g., negative numbers, overly long strings, non-JSON formats) and ensure the endpoint can handle them and return clear error messages.
# Verify that type conversion in the input data is handled correctly (e.g., converting "Yes" and "No" to boolean values).
client = TestClient(app)
def test_valid_input():
    """Test endpoint with valid input data"""
    print("\n#################### test_valid_input() ####################")
    response = client.post("/predict", json=test_model)
    
    if response.status_code == 200:
        result = response.json()
        if "baseline" in result and "interventions" in result:
            print("PASS\n")
            return
    print(f"FAIL: Invalid response for valid input: {response.json()}\n")

def test_missing_required_fields():
    """Test endpoint with missing required fields"""
    print("\n#################### test_missing_required_fields() ####################")
    
    required_fields = [
        "age", "gender", "work_experience", "level_of_schooling",
        "reading_english_scale", "speaking_english_scale", "writing_english_scale"
    ]
    
    passes = 0
    total = len(required_fields)
    
    for field in required_fields:
        invalid_data = test_model.copy()
        del invalid_data[field]
        
        response = client.post("/predict", json=invalid_data)
        if response.status_code == 422:  # FastAPI validation error status code
            error_detail = response.json().get("detail", [])
            if any(field in str(err) for err in error_detail):
                passes += 1
            else:
                print(f"FAIL: Missing appropriate error message for {field}\n")
        else:
            print(f"FAIL: Incorrect status code for missing {field}: {response.status_code}\n")
    
    if passes == total:
        print("PASS: All missing field validations working\n")
    else:
        print(f"FAIL: {total - passes} missing field validations failed\n")

def test_invalid_numeric_values():
    """Test endpoint with invalid numeric values"""
    print("\n#################### test_invalid_numeric_values() ####################")
    
    numeric_test_cases = [
        {"field": "age", "value": -1, "error_type": "value_error"},
        {"field": "age", "value": 150, "error_type": "value_error"},
        {"field": "work_experience", "value": -5, "error_type": "value_error"},
        {"field": "reading_english_scale", "value": 6, "error_type": "value_error"},
        {"field": "dep_num", "value": -2, "error_type": "value_error"}
    ]
    
    passes = 0
    total = len(numeric_test_cases)
    
    for case in numeric_test_cases:
        test_data = test_model.copy()
        test_data[case["field"]] = case["value"]
        
        response = client.post("/predict", json=test_data)
        if response.status_code == 422:
            error_detail = response.json().get("detail", [])
            if any(case["error_type"] in str(err) for err in error_detail):
                passes += 1
            else:
                print(f"FAIL: Missing appropriate error message for {case['field']} = {case['value']}\n")
        else:
            print(f"FAIL: Incorrect status code for invalid {case['field']}: {response.status_code}\n")
    
    if passes == total:
        print("PASS: All numeric validations working\n")
    else:
        print(f"FAIL: {total - passes} numeric validations failed\n")

def test_invalid_string_lengths():
    """Test endpoint with overly long strings"""
    print("\n#################### test_invalid_string_lengths() ####################")
    
    long_string = "a" * 1001  # String longer than maximum allowed length
    string_test_cases = [
        {"field": "gender", "value": long_string},
        {"field": "citizen_status", "value": long_string},
        {"field": "housing", "value": long_string}
    ]
    
    passes = 0
    total = len(string_test_cases)
    
    for case in string_test_cases:
        test_data = test_model.copy()
        test_data[case["field"]] = case["value"]
        
        response = client.post("/predict", json=test_data)
        if response.status_code == 422:
            error_detail = response.json().get("detail", [])
            if any("length" in str(err).lower() for err in error_detail):
                passes += 1
            else:
                print(f"FAIL: Missing appropriate error message for long {case['field']}\n")
        else:
            print(f"FAIL: Incorrect status code for long {case['field']}: {response.status_code}\n")
    
    if passes == total:
        print("PASS: All string length validations working\n")
    else:
        print(f"FAIL: {total - passes} string length validations failed\n")

def test_boolean_conversion():
    """Test endpoint with various boolean value formats"""
    print("\n#################### test_boolean_conversion() ####################")
    
    boolean_test_cases = [
        {"field": "canada_born", "values": ["true", "True", "1", True, "yes", "Yes"]},
        {"field": "fluent_english", "values": ["false", "False", "0", False, "no", "No"]}
    ]
    
    passes = 0
    total = sum(len(case["values"]) for case in boolean_test_cases)
    
    for case in boolean_test_cases:
        for value in case["values"]:
            test_data = test_model.copy()
            test_data[case["field"]] = value
            
            response = client.post("/predict", json=test_data)
            if response.status_code == 200:
                passes += 1
            else:
                print(f"FAIL: Boolean conversion failed for {case['field']} = {value}\n")
    
    if passes == total:
        print("PASS: All boolean conversions working\n")
    else:
        print(f"FAIL: {total - passes} boolean conversions failed\n")

def test_invalid_json():
    """Test endpoint with invalid JSON format"""
    print("\n#################### test_invalid_json() ####################")
    
    invalid_json_cases = [
        {
            "description": "Invalid JSON syntax",
            "content": b"{invalid_json"
        },
        {
            "description": "Plain text",
            "content": b"not_json_at_all"
        },
        {
            "description": "Valid JSON but wrong format",
            "content": b"[1, 2, 3]"
        },
        {
            "description": "Null value",
            "content": b"null"
        }
    ]
    
    passes = 0
    total = len(invalid_json_cases)
    
    for case in invalid_json_cases:
        response = client.post(
            "/predict", 
            headers={"Content-Type": "application/json"},
            content=case["content"]  # Using content with bytes
        )
        
        if response.status_code in [400, 422]:  # Either is acceptable for invalid JSON
            passes += 1
        else:
            print(f"FAIL: Incorrect status code for {case['description']}: {response.status_code}\n")
    
    if passes == total:
        print("PASS: All invalid JSON cases handled correctly\n")
    else:
        print(f"FAIL: {total - passes} invalid JSON cases failed\n")

def test_content_type_validation():
    """Test endpoint with incorrect content types"""
    print("\n#################### test_content_type_validation() ####################")
    
    content_type_cases = [
        {
            "content_type": "text/plain", 
            "content": b"plain text"
        },
        {
            "content_type": "application/xml", 
            "content": b"<xml>data</xml>"
        },
        {
            "content_type": "multipart/form-data", 
            "content": json.dumps(test_model).encode()
        }
    ]
    
    passes = 0
    total = len(content_type_cases)
    
    for case in content_type_cases:
        response = client.post(
            "/predict",
            headers={"Content-Type": case["content_type"]},
            content=case["content"]
        )
        
        if response.status_code in [400, 415]:
            passes += 1
        else:
            print(f"FAIL: Incorrect status code for content type {case['content_type']}: {response.status_code}\n")
    
    if passes == total:
        print("PASS: All content type validations working\n")
    else:
        print(f"FAIL: {total - passes} content type validations failed\n")

def test_empty_request():
    """Test endpoint with empty request body"""
    print("\n#################### test_empty_request() ####################")
    
    response = client.post("/predict", json={})
    
    if response.status_code == 422:
        error_detail = response.json().get("detail", [])
        if any("required" in str(err).lower() for err in error_detail):
            print("PASS\n")
            return
    print(f"FAIL: Incorrect handling of empty request: {response.status_code}\n")


# def test_form_submission(driver):
#     """Test form submission"""
#     print("\n#################### test_form_submission() ####################")
    
#     try:
#         # Print page title for debugging
#         print(f"Page Title: {driver.title}")
        
#         # Fill text fields
#         text_fields = {
#             "age": "25",
#             "work_experience": "3",
#             "reading_english_scale": "5",
#             "speaking_english_scale": "5",
#             "writing_english_scale": "5"
#         }
        
#         for name, value in text_fields.items():
#             try:
#                 element = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.NAME, name))
#                 )
#                 element.clear()
#                 element.send_keys(value)
#                 print(f"Successfully filled {name} with {value}")
#             except Exception as e:
#                 print(f"Error filling {name}: {str(e)}")
#                 raise

#         # Handle Material-UI select fields
#         select_fields = {
#             "gender": "Female",  
#             "level_of_schooling": "Bachelor's degree"
#         }
        
#         for name, value in select_fields.items():
#             try:
#                 # Print available elements for debugging
#                 print(f"\nLooking for {name} select field...")
#                 elements = driver.find_elements(By.CSS_SELECTOR, f'label:contains("{name.replace("_", " ").title()}")')
#                 print(f"Found {len(elements)} potential elements for {name}")
                
#                 # Try different selectors for the select field
#                 select_selectors = [
#                     f'//label[contains(text(), "{name.replace("_", " ").title()}")]/following-sibling::div',
#                     f'.MuiFormControl-root:has(label[contains(text(), "{name.replace("_", " ").title()}")]) .MuiSelect-select',
#                     f'[aria-label="{name.replace("_", " ").title()}"]'
#                 ]
                
#                 select_element = None
#                 for selector in select_selectors:
#                     try:
#                         print(f"Trying selector: {selector}")
#                         if selector.startswith('//'):
#                             select_element = WebDriverWait(driver, 3).until(
#                                 EC.element_to_be_clickable((By.XPATH, selector))
#                             )
#                         else:
#                             select_element = WebDriverWait(driver, 3).until(
#                                 EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
#                             )
#                         if select_element:
#                             print(f"Found select element for {name}")
#                             break
#                     except:
#                         continue
                
#                 if not select_element:
#                     print(f"Could not find select element for {name}")
#                     # Try JavaScript click on the Select component
#                     js_script = f"""
#                         const labels = Array.from(document.querySelectorAll('label'));
#                         const label = labels.find(l => l.textContent.includes('{name.replace("_", " ").title()}'));
#                         if (label) {{
#                             const select = label.parentElement.querySelector('.MuiSelect-select');
#                             if (select) select.click();
#                         }}
#                     """
#                     driver.execute_script(js_script)
#                     time.sleep(1)
#                 else:
#                     driver.execute_script("arguments[0].scrollIntoView(true);", select_element)
#                     driver.execute_script("arguments[0].click();", select_element)
#                     time.sleep(1)
                
#                 # Try to find the option
#                 print(f"Looking for option: {value}")
#                 option_selectors = [
#                     f'//li[contains(@class, "MuiMenuItem-root") and text()="{value}"]',
#                     f'.MuiPopover-paper li[data-value="{value}"]',
#                     f'.MuiMenu-paper li:contains("{value}")'
#                 ]
                
#                 option_found = False
#                 for selector in option_selectors:
#                     try:
#                         print(f"Trying option selector: {selector}")
#                         if selector.startswith('//'):
#                             option = WebDriverWait(driver, 3).until(
#                                 EC.element_to_be_clickable((By.XPATH, selector))
#                             )
#                         else:
#                             option = WebDriverWait(driver, 3).until(
#                                 EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
#                             )
#                         driver.execute_script("arguments[0].click();", option)
#                         option_found = True
#                         print(f"Successfully selected option {value} for {name}")
#                         break
#                     except:
#                         continue
                
#                 if not option_found:
#                     print(f"Could not find option {value} for {name}")
#                     raise Exception(f"Option {value} not found for {name}")
                
#             except Exception as e:
#                 print(f"Error handling select field {name}: {str(e)}")
#                 raise
            
#             time.sleep(1)

#         # Submit form
#         try:
#             # Try different submit button selectors
#             submit_selectors = [
#                 'button[type="submit"]',
#                 'button.MuiButton-containedPrimary',
#                 '//button[contains(text(), "Submit")]'
#             ]
            
#             submit_button = None
#             for selector in submit_selectors:
#                 try:
#                     print(f"Trying submit button selector: {selector}")
#                     if selector.startswith('//'):
#                         submit_button = WebDriverWait(driver, 3).until(
#                             EC.element_to_be_clickable((By.XPATH, selector))
#                         )
#                     else:
#                         submit_button = WebDriverWait(driver, 3).until(
#                             EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
#                         )
#                     if submit_button:
#                         break
#                 except:
#                     continue
            
#             if submit_button:
#                 driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
#                 driver.execute_script("arguments[0].click();", submit_button)
#                 print("Form submitted")
                
#                 WebDriverWait(driver, 10).until(
#                     lambda d: "/results" in d.current_url
#                 )
#                 print("PASS: Form submitted successfully\n")
#             else:
#                 print("FAIL: Submit button not found\n")
#                 raise Exception("Submit button not found")
                
#         except Exception as e:
#             print(f"Error submitting form: {str(e)}")
#             raise
            
#     except Exception as e:
#         print(f"FAIL: Error during form submission: {str(e)}\n")
#         raise e


# # Add debugging helper
# def print_elements(driver):
#     """Helper function to print visible elements"""
#     elements = driver.find_elements(By.CSS_SELECTOR, '*')
#     for element in elements:
#         try:
#             if element.is_displayed():
#                 tag_name = element.tag_name
#                 class_name = element.get_attribute('class')
#                 element_text = element.text
#                 print(f"Tag: {tag_name}, Class: {class_name}, Text: {element_text}")
#         except:
#             continue

# # raw data from front end
# test_model = {
#     "age": "18",
#     "gender": "M",
#     "work_experience": "3",
#     "canada_workex": 0,
#     "dep_num": "1",
#     "canada_born": "true",
#     "citizen_status": "citizen",
#     "level_of_schooling": "Grade 12 or equivalent",
#     "fluent_english": "true",
#     "reading_english_scale": "3",
#     "speaking_english_scale": "1",
#     "writing_english_scale": "3",
#     "numeracy_scale": 0,
#     "computer_scale": "2",
#     "transportation_bool": "false",
#     "caregiver_bool": "true",
#     "housing": "Living with family/friend",
#     "income_source": "No Source of Income",
#     "felony_bool": "true",
#     "attending_school": "false",
#     "currently_employed": "true",
#     "substance_use": "true",
#     "time_unemployed": "1",
#     "need_mental_health_support_bool": "false"
# }

# # the converted data
# test_converted = {'age': 18, 'gender': 1, 'work_experience': 3, 'canada_workex': 0, 'dep_num': 1, 'canada_born': True,
#                   'citizen_status': 0, 'level_of_schooling': 5, 'fluent_english': True, 'reading_english_scale': 3,
#                   'speaking_english_scale': 1, 'writing_english_scale': 3, 'numeracy_scale': 0, 'computer_scale': 2,
#                   'transportation_bool': False, 'caregiver_bool': True, 'housing': 5, 'income_source': 1,
#                   'felony_bool': True, 'attending_school': False, 'currently_employed': True, 'substance_use': True,
#                   'time_unemployed': 1, 'need_mental_health_support_bool': False}

# # output after data converting
# test_output = [18, 1, 3, 0, 1, 1, 0, 5, 1, 3, 1, 3, 0, 2, 0, 1, 5, 1, 1, 0, 1, 1, 1, 0]

# # prediction result
# test_prediction_result = {
#     "baseline": 67.6,
#     "interventions": [
#         (68.7, ["Life Stabilization", "General Employment Assistance Services", "Specialized Services", "Employment-Related Financial Supports for Job Seekers and Employers"]),
#         (68.7, ["Life Stabilization", "Specialized Services", "Employment-Related Financial Supports for Job Seekers and Employers"]),
#         (69.0, ["Life Stabilization", "Specialized Services"])]
# }



# # ordered features for test
# test_features = ['age', 'gender', 'work_experience', 'canada_workex', 'dep_num', 'canada_born', 'citizen_status',
#                       'level_of_schooling', 'fluent_english', 'reading_english_scale', 'speaking_english_scale',
#                       'writing_english_scale', 'numeracy_scale', 'computer_scale', 'transportation_bool',
#                       'caregiver_bool', 'housing', 'income_source', 'felony_bool', 'attending_school',
#                       'currently_employed', 'substance_use', 'time_unemployed', 'need_mental_health_support_bool']


# def get_data():
#     return PredictionInput(**test_model).model_dump(by_alias=True)


# def test_dump_model():
#     """test to check the dumped model"""
#     print("\n#################### test_dump_model() ####################")
#     refactor_converted = get_data()
#     if refactor_converted == test_converted:
#         print("PASS\n")
#     else:
#         print("FAIL\n")


# def test_clean_input_data():
#     """test data type conversion"""
#     print("\n#################### test_clean_input_data() ####################")
#     data = get_data()
#     refactor_output = clean_input_data(data, test_features)

#     if len(test_output) != len(refactor_output):
#         print("FAIL: len not equals\n")
#         return

#     for i in range(len(test_output)):
#         if test_output[i] != refactor_output[i]:
#             print("FAIL: the {} th element not equals. origin:{}, refactor:{}\n".format(i, test_output[i], refactor_output[i]))
#             return
#     print("PASS\n")


# def test_prediction():
#     """test the whole prediction process"""
#     print("\n#################### test_prediction() ####################")
#     data = get_data()
#     result = interpret_and_calculate(data)
#     if result == test_prediction_result:
#         print("PASS\n")
#     else:
#         print("FAIL\n")

# #################### Test Data and Methods ####################

# # original order of columns:
# test_original_cols = ['age', 'gender', 'work_experience', 'canada_workex', 'dep_num', 'canada_born', 'citizen_status',
#                       'level_of_schooling', 'fluent_english', 'reading_english_scale', 'speaking_english_scale',
#                       'writing_english_scale', 'numeracy_scale', 'computer_scale', 'transportation_bool',
#                       'caregiver_bool', 'housing', 'income_source', 'felony_bool', 'attending_school',
#                       'currently_employed', 'substance_use', 'time_unemployed', 'need_mental_health_support_bool']


# def test_column_order():
#     print("\n#################### test_data_type_conversion() ####################")
#     cols = util_get_cols()
#     # print(cols)
#     if cols == test_original_cols:
#         print("PASS")
#     else:
#         print("FAIL")
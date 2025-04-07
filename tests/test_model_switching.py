import pytest
from fastapi.testclient import TestClient
from app.main import app

# Use pytest fixture for creating the TestClient instance
@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

# Use pytest fixture for admin headers
@pytest.fixture
def test_admin_headers():
    return {"Authorization": "Bearer YOUR_ADMIN_TOKEN"}

# Test switching to a valid model
def test_switch_model_valid(test_client, test_admin_headers):
    response = test_client.post(
        "/ml/switch-model", json={"model_name": "decision_tree"}, headers=test_admin_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Model switched to decision_tree",
    }

# Test switching to an invalid model
def test_switch_model_invalid(test_client, test_admin_headers):
    response = test_client.post(
        "/ml/switch-model", json={"model_name": "invalid_model"}, headers=test_admin_headers
    )
    assert response.status_code == 400
    assert response.json() == {
        "status": "error",
        "message": "Model 'invalid_model' is not available.",
    }

# Test getting the current active model
def test_get_current_model(test_client, test_admin_headers):
    response = test_client.get("/ml/current-model", headers=test_admin_headers)
    assert response.status_code == 200
    assert "current_model" in response.json()

# Test prediction with valid data after switching the model
def test_prediction(test_client, test_admin_headers):
    data = {
        "age": 30,
        "gender": "2",
        "work_experience": 5,
        "canada_workex": 2,
        "dep_num": 1,
        "canada_born": "true",
        "citizen_status": "true",
        "level_of_schooling": "8",
        "fluent_english": "true",
        "reading_english_scale": 8,
        "speaking_english_scale": 7,
        "writing_english_scale": 7,
        "numeracy_scale": 8,
        "computer_scale": 9,
        "transportation_bool": "true",
        "caregiver_bool": "false",
        "housing": "5",
        "income_source": "3",
        "felony_bool": "false",
        "attending_school": "false",
        "currently_employed": "false",
        "substance_use": "false",
        "time_unemployed": 6,
        "need_mental_health_support_bool": "false",
    }
    response = test_client.post("/ml/predict", json=data, headers=test_admin_headers)
    print(response.json())
    assert response.status_code == 200
    assert "prediction" in response.json()  # Ensure the response contains the prediction

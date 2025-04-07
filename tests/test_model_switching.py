import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def admin_headers():
    # Assume you already have the admin token or headers set up here
    return {"Authorization": "Bearer YOUR_ADMIN_TOKEN"}


def test_switch_model_valid(client, admin_headers):
    # Test that switching to a valid model works
    response = client.post(
        "/ml/switch-model", json={"model_name": "decision_tree"}, headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Model switched to decision_tree",
    }


def test_switch_model_invalid(client, admin_headers):
    # Test that switching to an invalid model returns an error
    response = client.post(
        "/ml/switch-model", json={"model_name": "invalid_model"}, headers=admin_headers
    )
    assert response.status_code == 400
    assert response.json() == {
        "status": "error",
        "message": "Model 'invalid_model' is not available.",
    }


def test_get_current_model(client, admin_headers):
    # Test getting the current active model
    response = client.get("/ml/current-model", headers=admin_headers)
    assert response.status_code == 200
    assert "current_model" in response.json()


def test_prediction(client, admin_headers):
    # Test prediction with valid data after switching model
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

    response = client.post("/ml/predict", json=data, headers=admin_headers)
    print(response.json())
    assert response.status_code == 200
    assert (
        "prediction" in response.json()
    )  # Ensure the response contains the prediction

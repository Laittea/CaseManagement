import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test for creating a user
def test_create_user():
    payload = {
        "age": 30,
        "gender": "male",
        "work_experience": 5,
        "canada_workex": 2,
        "dep_num": 0,
        "canada_born": "yes",
        "citizen_status": "citizen",
        "level_of_schooling": "bachelor",
        "fluent_english": "yes",
        "reading_english_scale": 5,
        "speaking_english_scale": 5,
        "writing_english_scale": 5,
        "numeracy_scale": 4,
        "computer_scale": 5,
        "transportation_bool": "yes",
        "caregiver_bool": "no",
        "housing": "rented",
        "income_source": "employment",
        "felony_bool": "no",
        "attending_school": "no",
        "currently_employed": "yes",
        "substance_use": "no",
        "time_unemployed": 0,
        "need_mental_health_support_bool": "no"
    }
    response = client.post("/clients/create-user", json=payload)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["message"] == "User created successfully"

    # Validate that the response includes the correct user data
    user = response_data["user"]
    for key in payload.keys():
        assert user[key] == payload[key]

# Test for getting all users
def test_get_all_users():
    response = client.get("/clients/users")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)

    # Ensure at least one user exists
    assert len(response_data) > 0

    # Validate the structure of the first user in the list
    user = response_data[0]
    expected_keys = [
        "id", "age", "gender", "work_experience", "canada_workex", "dep_num",
        "canada_born", "citizen_status", "level_of_schooling", "fluent_english",
        "reading_english_scale", "speaking_english_scale", "writing_english_scale",
        "numeracy_scale", "computer_scale", "transportation_bool", "caregiver_bool",
        "housing", "income_source", "felony_bool", "attending_school",
        "currently_employed", "substance_use", "time_unemployed",
        "need_mental_health_support_bool"
    ]
    for key in expected_keys:
        assert key in user

# Test for getting a user by ID
def test_get_user_by_id():
    # Adjust ID based on your database setup
    user_id = 1
    response = client.get(f"/clients/users/{user_id}")
    if response.status_code == 200:
        user = response.json()
        assert user["id"] == user_id
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "Client not found"

# Test for updating a user
def test_update_user():
    # Adjust ID based on your database setup
    user_id = 1
    payload = {
        "age": 35,
        "gender": "female",
        "work_experience": 10,
        "canada_workex": 5,
        "dep_num": 2,
        "canada_born": "no",
        "citizen_status": "permanent_resident",
        "level_of_schooling": "master",
        "fluent_english": "yes",
        "reading_english_scale": 4,
        "speaking_english_scale": 4,
        "writing_english_scale": 4,
        "numeracy_scale": 4,
        "computer_scale": 5,
        "transportation_bool": "no",
        "caregiver_bool": "yes",
        "housing": "owned",
        "income_source": "self_employment",
        "felony_bool": "no",
        "attending_school": "no",
        "currently_employed": "yes",
        "substance_use": "no",
        "time_unemployed": 0,
        "need_mental_health_support_bool": "yes"
    }
    response = client.put(f"/clients/users/{user_id}", json=payload)
    if response.status_code == 200:
        assert response.json()["message"] == "User updated successfully"

        # Validate updated data
        updated_user = client.get(f"/clients/users/{user_id}").json()
        for key in payload.keys():
            assert updated_user[key] == payload[key]
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "Client not found"

# Test for deleting a user
def test_delete_user():
    # Adjust ID based on your database setup
    user_id = 1
    response = client.delete(f"/clients/users/{user_id}")
    if response.status_code == 200:
        assert response.json()["message"] == "Client deleted successfully"

        # Ensure the user no longer exists
        get_response = client.get(f"/clients/users/{user_id}")
        assert get_response.status_code == 404
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "Client not found"

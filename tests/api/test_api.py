import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.schema.schema import UserCreate, CandidateCreate, DetailedInfoCreate

# Set up test database (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the `get_db` dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Initialize test client
client = TestClient(app)

# Create tables for the test database
Base.metadata.create_all(bind=engine)

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    # Code to run before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Code to run after each test
    Base.metadata.drop_all(bind=engine)

### User Route Tests ###

def test_create_user_route():
    response = client.post("/users/", json={"name": "Test User", "email": "testuser@example.com", "password": "password123", "role": "user"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"
    assert response.json()["email"] == "testuser@example.com"

def test_get_user_route():
    # First, create a user
    client.post("/users/", json={"name": "Test User", "email": "testuser@example.com", "password": "password123", "role": "user"})
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

def test_get_user_not_found():
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_users_route():
    client.post("/users/", json={"name": "User One", "email": "user1@example.com", "password": "password123", "role": "user"})
    client.post("/users/", json={"name": "User Two", "email": "user2@example.com", "password": "password123", "role": "admin"})
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_delete_user_route():
    client.post("/users/", json={"name": "Test User", "email": "testuser@example.com", "password": "password123", "role": "user"})
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

def test_delete_user_not_found():
    response = client.delete("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

### Candidate Route Tests ###

def test_create_candidate_route():
    client.post("/users/", json={"name": "Test User", "email": "testuser@example.com", "password": "password123", "role": "user"})
    response = client.post("/candidates/", json={"applicationDate": "2024-11-15", "applicationStatus": "Pending", "user_id": "testuser@example.com"})
    assert response.status_code == 200
    assert response.json()["application_status"] == "Pending"

def test_get_candidate_route():
    client.post("/users/", json={"name": "Test User", "email": "testuser@example.com", "password": "password123", "role": "user"})
    client.post("/candidates/", json={"applicationDate": "2024-11-15", "applicationStatus": "Pending", "user_id": "testuser@example.com"})
    response = client.get("/candidates/1")
    assert response.status_code == 200
    assert response.json()["application_status"] == "Pending"

def test_get_candidate_not_found():
    response = client.get("/candidates/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidate not found"

def test_delete_candidate_route():
    client.post("/users/", json={"name": "Test User", "email": "testuser@example.com", "password": "password123", "role": "user"})
    client.post("/candidates/", json={"applicationDate": "2024-11-15", "applicationStatus": "Pending", "user_id": "testuser@example.com"})
    response = client.delete("/candidates/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Candidate deleted successfully"

def test_delete_candidate_not_found():
    response = client.delete("/candidates/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidate not found"

### DetailedInfo Route Tests ###

def test_create_detailed_info_route():
    client.post("/users/", json={"name": "Test User", "email": "testuser@example.com", "password": "password123", "role": "user"})
    client.post("/candidates/", json={"applicationDate": "2024-11-15", "applicationStatus": "Pending", "user_id": "testuser@example.com"})
    response = client.post("/detailed_info/", json={
        "attendingSchool": True,
        "levelOfSchooling": 5,
        "fluentEnglishScale": 3,
        "readingEnglishScale": 2,
        "speakingEnglishScale": 3,
        "writingEnglishScale": 3,
        "numeracyScale": 2,
        "computerScale": 3,
        "workExperience": 5,
        "canadaWorkEx": 1,
        "currentlyEmployed": True,
        "incomeSource": 8,
        "timeUnemployed": 2,
        "substance_use": False,
        "caregiverBool": True,
        "housingBool": 1,
        "needMentalHealthSupportBool": False,
        "transportationBool": True,
        "felonyBool": False
    }, params={"candidate_id": 1})
    assert response.status_code == 200
    assert response.json()["attending_school"] is True

def test_get_detailed_info_by_candidate_route():
    client.post("/users/", json={"name": "Test User", "email": "testuser@example.com", "password": "password123", "role": "user"})
    client.post("/candidates/", json={"applicationDate": "2024-11-15", "applicationStatus": "Pending", "user_id": "testuser@example.com"})
    client.post("/detailed_info/", json={
        "attendingSchool": True,
        "levelOfSchooling": 5,
        "fluentEnglishScale": 3,
        "readingEnglishScale": 2,
        "speakingEnglishScale": 3,
        "writingEnglishScale": 3,
        "numeracyScale": 2,
        "computerScale": 3,
        "workExperience": 5,
        "canadaWorkEx": 1,
        "currentlyEmployed": True,
        "incomeSource": 8,
        "timeUnemployed": 2,
        "substance_use": False,
        "caregiverBool": True,
        "housingBool": 1,
        "needMentalHealthSupportBool": False,
        "transportationBool": True,
        "felonyBool": False
    }, params={"candidate_id": 1})
    response = client.get("/detailed_info/1")
    assert response.status_code == 200
    assert response.json()["attending_school"] is True

def test_delete_detailed_info_route():
    client.post("/users/", json={"name": "Test User", "email": "testuser@example.com", "password": "password123", "role": "user"})
    client.post("/candidates/", json={"applicationDate": "2024-11-15", "applicationStatus": "Pending", "user_id": "testuser@example.com"})
    client.post("/detailed_info/", json={
        "attendingSchool": True,
        "levelOfSchooling": 5,
        "fluentEnglishScale": 3,
        "readingEnglishScale": 2,
        "speakingEnglishScale": 3,
        "writingEnglishScale": 3,
        "numeracyScale": 2,
        "computerScale": 3,
        "workExperience": 5,
        "canadaWorkEx": 1,
        "currentlyEmployed": True,
        "incomeSource": 8,
        "timeUnemployed": 2,
        "substance_use": False,
        "caregiverBool": True,
        "housingBool": 1,
        "needMentalHealthSupportBool": False,
        "transportationBool": True,
        "felonyBool": False
    }, params={"candidate_id": 1})
    response = client.delete("/detailed_info/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Detailed info deleted successfully"

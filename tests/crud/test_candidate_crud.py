import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.model import Base, User, Candidate, UserRole
from app.schema.schema import CandidateCreate
from app.crud.candidate_crud import (
    create_candidate,
    get_candidate,
    get_all_candidates,
    update_application_status,
    delete_candidate,
)
from app.exceptions import UserNotFoundError

# Shared Test Database Engine
engine = create_engine("sqlite:///:memory:")  # In-memory database

# Test Database Setup
@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def setup_test_user(test_db):
    unique_email = f"testuser_{id(test_db)}@example.com"
    user = User(name="Test User", email=unique_email, password="password123", role=UserRole.CANDIDATE)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

def test_create_candidate_success(test_db, setup_test_user):
    user = setup_test_user
    candidate_data = CandidateCreate(
        user_id=user.id,
        name=user.name,  # Include name
        email=user.email,  # Include email
        applicationDate=datetime.now(),
        applicationStatus="Pending"
    )

    candidate_response = create_candidate(test_db, candidate_data)

    assert candidate_response.id is not None
    assert candidate_response.applicationStatus == "Pending"
    assert candidate_response.name == user.name
    assert candidate_response.email == user.email

def test_create_candidate_user_not_found(test_db):
    candidate_data = CandidateCreate(
        user_id=999,
        name="Nonexistent User",  # Include name
        email="nonexistent@example.com",  # Include email
        applicationDate=datetime.now(),
        applicationStatus="Pending"
    )
    with pytest.raises(UserNotFoundError):
        create_candidate(test_db, candidate_data)

def test_get_candidate_success(test_db, setup_test_user):
    user = setup_test_user
    candidate = Candidate(user_id=user.id, application_date=datetime.now(), application_status="Pending")
    test_db.add(candidate)
    test_db.commit()
    test_db.refresh(candidate)

    candidate_response = get_candidate(test_db, candidate.id)

    assert candidate_response.id == candidate.id
    assert candidate_response.applicationStatus == "Pending"
    assert candidate_response.user["email"] == user.email

def test_get_candidate_not_found(test_db):
    with pytest.raises(UserNotFoundError):
        get_candidate(test_db, 999)

def test_get_all_candidates(test_db, setup_test_user):
    user = setup_test_user
    candidates = [
        Candidate(user_id=user.id, application_date=datetime.now(), application_status="Pending"),
        Candidate(user_id=user.id, application_date=datetime.now(), application_status="Approved"),
    ]
    test_db.add_all(candidates)
    test_db.commit()

    all_candidates = get_all_candidates(test_db)

    assert len(all_candidates) == 2
    assert all_candidates[0].name == user.name
    assert all_candidates[0].email == user.email
    assert all_candidates[0].applicationStatus == "Pending"
    assert all_candidates[1].applicationStatus == "Approved"

def test_update_application_status_success(test_db, setup_test_user):
    user = setup_test_user
    candidate = Candidate(user_id=user.id, application_date=datetime.now(), application_status="Pending")
    test_db.add(candidate)
    test_db.commit()
    test_db.refresh(candidate)

    updated_candidate = update_application_status(test_db, candidate.id, "Approved")

    assert updated_candidate.id == candidate.id
    assert updated_candidate.applicationStatus == "Approved"
    assert updated_candidate.name == user.name
    assert updated_candidate.email == user.email

def test_update_application_status_candidate_not_found(test_db):
    with pytest.raises(UserNotFoundError):
        update_application_status(test_db, 999, "Approved")

def test_delete_candidate_success(test_db, setup_test_user):
    user = setup_test_user
    candidate = Candidate(user_id=user.id, application_date=datetime.now(), application_status="Pending")
    test_db.add(candidate)
    test_db.commit()
    test_db.refresh(candidate)

    assert delete_candidate(test_db, candidate.id) is True
    assert test_db.query(Candidate).filter_by(id=candidate.id).first() is None

def test_delete_candidate_not_found(test_db):
    assert delete_candidate(test_db, 999) is False  # Non-existent candidate ID

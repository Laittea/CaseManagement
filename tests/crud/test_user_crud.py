import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.model import Base, User, UserRole
from app.schema.schema import UserCreate
from app.crud.user_crud import (
    get_user,
    get_users,
    create_user,
    delete_user,
)

# Setup test database
@pytest.fixture(scope="function")
def test_db():
    engine = create_engine("sqlite:///:memory:")  # Use SQLite in-memory database for testing
    Base.metadata.create_all(engine)  # Create tables
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(engine)  # Clean up the database

# Test `create_user`
def test_create_user(test_db):
    user_data = UserCreate(
        name="Test User",
        email="testuser@example.com",
        password="securepassword",
        role=UserRole.CANDIDATE,
    )
    new_user = create_user(test_db, user_data)
    assert new_user.id is not None
    assert new_user.name == "Test User"
    assert new_user.email == "testuser@example.com"
    assert new_user.role == UserRole.CANDIDATE

# Test `get_user`
def test_get_user(test_db):
    user = User(name="Test User", email="testuser@example.com", password="securepassword", role=UserRole.RECRUITER)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    retrieved_user = get_user(test_db, user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == user.id
    assert retrieved_user.name == "Test User"
    assert retrieved_user.email == "testuser@example.com"

# Test `get_users`
def test_get_users(test_db):
    users = [
        User(name="User One", email="user1@example.com", password="password1", role=UserRole.ADMIN),
        User(name="User Two", email="user2@example.com", password="password2", role=UserRole.CANDIDATE),
    ]
    test_db.add_all(users)
    test_db.commit()

    retrieved_users = get_users(test_db, skip=0, limit=10)
    assert len(retrieved_users) == 2
    assert retrieved_users[0].name == "User One"
    assert retrieved_users[1].name == "User Two"

# Test `delete_user`
def test_delete_user(test_db):
    user = User(name="Deletable User", email="delete@example.com", password="deletepassword", role=UserRole.RECRUITER)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    deleted_user = delete_user(test_db, user.id)
    assert deleted_user is not None
    assert deleted_user.id == user.id

    # Ensure the user is no longer in the database
    assert get_user(test_db, user.id) is None

# Test `delete_user` when the user does not exist
def test_delete_nonexistent_user(test_db):
    deleted_user = delete_user(test_db, 999)  # Non-existent user ID
    assert deleted_user is None
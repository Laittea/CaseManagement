"""
CRUD operations for User model.

This module contains the following CRUD functions for managing users:

- get_user: Retrieve a user by their unique ID.
- get_users: Retrieve a list of users, with optional pagination.
- create_user: Create a new user in the database.
- delete_user: Delete a user by their unique ID.

Each function interacts with the database session to perform operations related to users.
"""

from sqlalchemy.orm import Session
from app.models.model import User
from app.schema.schema import UserCreate

def get_user(db: Session, user_id: int):
    """
    Retrieve a user by their unique ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to be retrieved.

    Returns:
        User | None: The user object if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of users, with optional pagination.

    Args:
        db (Session): The database session.
        skip (int, optional): The number of users to skip (default is 0).
        limit (int, optional): The maximum number of users to retrieve (default is 10).

    Returns:
        List[User]: A list of users within the specified limit.
    """

    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data to be added.

    Returns:
        User: The created user object.
    """
    db_user = User(name=user.name, email=user.email, password=user.password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """
    Delete a user by their unique ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to be deleted.

    Returns:
        User | None: The deleted user object if found, otherwise None.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

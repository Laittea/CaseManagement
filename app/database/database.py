"""
Database setup and session management for SQLAlchemy.

This module provides the following:

- `Base`: SQLAlchemy's declarative base for model definitions.
- `engine`: SQLAlchemy engine for connecting to the database, configured with the `DATABASE_URL`.
- `SessionLocal`: SQLAlchemy session maker for creating database sessions.
- `get_db`: A dependency that yields a database session for use in route handlers.

The module is responsible for setting up the connection to the database,
creating models, and managing the database session lifecycle.
"""

# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL  # Importing the database URL from config

# SQLAlchemy Base class for model definitions
Base = declarative_base()

# Create the SQLite database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)  # `check_same_thread` is needed for SQLite

# SessionLocal instance for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    """
        Dependency to get a database session.

        This function is used as a dependency in FastAPI route
        handlers to provide a database session.

        Yields:
            Session: A database session instance,
                     which should be used to interact with the database.

        The session is automatically closed after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

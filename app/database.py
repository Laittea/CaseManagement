"""
Database configuration module for the Common Assessment Tool.
Handles database connection and session management using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import DATABASE_URL

# Open up a connection so that we are able to use the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Bind the engine just created
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create an object of our database so as to control the database
Base = declarative_base()


def get_db():
    """
    Creates a database session and ensures it's closed after use.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

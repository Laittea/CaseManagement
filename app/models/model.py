# models.py

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.databse import Base


# Enum classes for role types
class UserRole(PyEnum):
    RECRUITER = "recruiter"
    ADMIN = "admin"
    CANDIDATE = "candidate"


# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    # Relationships
    candidate = relationship("Candidate", back_populates="user")
    recruiter = relationship("Recruiter", back_populates="user")
    admin = relationship("Admin", back_populates="user")


# Candidate model
class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    application_date = Column(DateTime, nullable=False)
    application_status = Column(String, nullable=False)

    # Relationship
    user = relationship("User", back_populates="candidate")
    detailed_info = relationship("DetailedInfo", back_populates="candidate")


# Recruiter model
class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship
    user = relationship("User", back_populates="recruiter")


# Admin model
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship
    user = relationship("User", back_populates="admin")


# DetailedInfo model
class DetailedInfo(Base):
    __tablename__ = "detailed_info"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))

    # Education-related attributes
    attending_school = Column(String)
    level_of_schooling = Column(String)
    fluent_english = Column(String)
    reading_english_scale = Column(Integer)
    speaking_english_scale = Column(Integer)
    writing_english_scale = Column(Integer)
    numeracy_scale = Column(Integer)
    computer_scale = Column(Integer)

    # Employment-related attributes
    work_experience = Column(Integer)
    canada_work_ex = Column(Integer)
    currently_employed = Column(String)
    income_source = Column(String)
    time_unemployed = Column(Integer)
    substance_use = Column(String)

    # Support needs-related attributes
    caregiver_bool = Column(String)
    housing_bool = Column(String)
    need_mental_health_support_bool = Column(String)
    transportation_bool = Column(String)

    # Criminal history-related attribute
    felony_bool = Column(String)

    # Relationship
    candidate = relationship("Candidate", back_populates="detailed_info")

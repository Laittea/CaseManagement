# pylint: disable=too-few-public-methods

"""
Database models for users, candidates, recruiters, and admins.

This module defines the following models using SQLAlchemy's ORM system:

- `User`: Represents a user with different roles (recruiter, admin, candidate).
- `Candidate`: Represents a candidate,
            linked to a user and containing detailed application information.
- `Recruiter`: Represents a recruiter, linked to a user.
- `Admin`: Represents an admin, linked to a user.
- `DetailedInfo`: Stores detailed information for candidates,
            such as educational background, language proficiency, work experience, and more.

The relationships between these models are established using SQLAlchemy's
`relationship` function and foreign keys, with cascading deletes enabled for related records.

Enumerated values for user roles are managed using the `UserRole` enum class.
"""

from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class UserRole(PyEnum):
    """
    Enum to define the roles of a user in the system.

    The available roles are:
    - `RECRUITER`: A user who is a recruiter.
    - `ADMIN`: A user who has admin privileges.
    - `CANDIDATE`: A user who is a candidate applying for jobs.
    """
    RECRUITER = "recruiter"
    ADMIN = "admin"
    CANDIDATE = "candidate"


class User(Base):
    """
    Represents a user in the system.

    Attributes:
    - `id`: Unique identifier for the user.
    - `name`: Name of the user.
    - `email`: Email address of the user, must be unique.
    - `password`: User's password for authentication.
    - `role`: Role of the user, determined by the `UserRole` enum.

    Relationships:
    - `candidate`: Links to the `Candidate` model, one-to-one relationship.
    - `recruiter`: Links to the `Recruiter` model, one-to-one relationship.
    - `admin`: Links to the `Admin` model, one-to-one relationship.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    candidate = relationship(
        "Candidate",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )
    recruiter = relationship(
        "Recruiter",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )
    admin = relationship(
        "Admin",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )


class Candidate(Base):
    """
    Represents a candidate applying for jobs.

    Attributes:
    - `id`: Unique identifier for the candidate.
    - `user_id`: Foreign key to the `User` model.
    - `application_date`: Date when the candidate applied.
    - `application_status`: Current application status (e.g., "pending", "approved", "rejected").

    Relationships:
    - `user`: Links to the `User` model, one-to-one relationship.
    - `detailed_info`: Links to the `DetailedInfo` model, one-to-many relationship
                       (a candidate can have detailed information).
    """
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    application_date = Column(DateTime, nullable=False)
    application_status = Column(String, nullable=False)
    user = relationship("User", back_populates="candidate")
    detailed_info = relationship(
        "DetailedInfo",
        back_populates="candidate",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Recruiter(Base):
    """
    Represents a recruiter in the system.

    Attributes:
    - `id`: Unique identifier for the recruiter.
    - `user_id`: Foreign key to the `User` model.

    Relationships:
    - `user`: Links to the `User` model, one-to-one relationship.
    """
    __tablename__ = "recruiters"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="recruiter")


class Admin(Base):
    """
    Represents an admin in the system.

    Attributes:
    - `id`: Unique identifier for the admin.
    - `user_id`: Foreign key to the `User` model.

    Relationships:
    - `user`: Links to the `User` model, one-to-one relationship.
    """
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="admin")


class DetailedInfo(Base):
    """
    Stores detailed information for candidates.

    Attributes:
    - `id`: Unique identifier for the detailed info record.
    - `candidate_id`: Foreign key to the `Candidate` model.
    - `attending_school`: Name of the school the candidate is attending (if any).
    - `level_of_schooling`: Education level of the candidate.
    - `fluent_english_scale`: Candidate's fluency in English.
    - `reading_english_scale`: Candidate's reading proficiency in English (scale).
    - `speaking_english_scale`: Candidate's speaking proficiency in English (scale).
    - `writing_english_scale`: Candidate's writing proficiency in English (scale).
    - `numeracy_scale`: Candidate's numeracy proficiency (scale).
    - `computer_scale`: Candidate's computer proficiency (scale).
    - `work_experience`: Years of work experience the candidate has.
    - `canada_work_ex`: Years of work experience in Canada.
    - `currently_employed`: Whether the candidate is currently employed.
    - `income_source`: Primary source of income for the candidate.
    - `time_unemployed`: Time (in months) the candidate has been unemployed.
    - `substance_use`: Whether the candidate uses substances.
    - `caregiver_bool`: Whether the candidate is a caregiver.
    - `housing_bool`: Whether the candidate has housing.
    - `need_mental_health_support_bool`: Whether the candidate needs mental health support.
    - `transportation_bool`: Whether the candidate has transportation.
    - `felony_bool`: Whether the candidate has a felony.

    Relationships:
    - `candidate`: Links to the `Candidate` model, one-to-one relationship.
    """
    __tablename__ = "detailed_info"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    candidate = relationship("Candidate", back_populates="detailed_info")
    attending_school = Column(String)
    level_of_schooling = Column(String)
    fluent_english_scale = Column(String)
    reading_english_scale = Column(Integer)
    speaking_english_scale = Column(Integer)
    writing_english_scale = Column(Integer)
    numeracy_scale = Column(Integer)
    computer_scale = Column(Integer)
    work_experience = Column(Integer)
    canada_work_ex = Column(Integer)
    currently_employed = Column(String)
    income_source = Column(String)
    time_unemployed = Column(Integer)
    substance_use = Column(String)
    caregiver_bool = Column(String)
    housing_bool = Column(String)
    need_mental_health_support_bool = Column(String)
    transportation_bool = Column(String)
    felony_bool = Column(String)

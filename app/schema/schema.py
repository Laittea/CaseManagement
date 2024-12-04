# pylint: disable=too-few-public-methods, C0115, W0107

"""
Schemas for users, candidates, recruiters, admins, and detailed candidate information.

This module defines Pydantic models for the following entities:

- `User`: Represents a user in the system with attributes
          like `name`, `email`, and `role`.
- `Candidate`: Represents a job candidate,
               extending `User` and adding application-specific fields.
- `Recruiter`: Represents a recruiter,
               extending `User` with the ability to create and manage job postings.
- `Admin`: Represents an admin, extending `User` with administrative privileges.
- `DetailedInfo`: Stores detailed information about a candidate,
                  including education, work experience, and personal traits.

The models are used for creating, updating, and responding to API requests and responses.
They leverage Pydantic’s `BaseModel` for data validation and serialization,
including the use of `orm_mode` for mapping data between the database and Pydantic models.

Functions in this module are primarily used to validate
and transform the data for creating or responding to user-related entities in the system.

Classes:
- `UserBase`: Base class for user-related schemas,
              defining common attributes.
- `UserCreate`: Inherits from `UserBase` and
                includes the password and role for creating a user.
- `UserResponse`: Inherits from `UserBase` and
                  includes the `id` for user responses.
- `CandidateBase`: Base class for candidate-related schemas,
                   adding `applicationDate` and `applicationStatus`.
- `CandidateCreate`: Inherits from `CandidateBase` with
                     the addition of `user_id` for creating a candidate.
- `CandidateResponse`: Inherits from `CandidateBase` and
                       includes a nested `user` dictionary for responses.
- `RecruiterBase`: Base class for recruiter-related schemas,
                   extending `UserBase` with `user_id`.
- `RecruiterCreate`: Inherits from `RecruiterBase` and
                     includes the password for creating a recruiter.
- `RecruiterResponse`: Inherits from `RecruiterBase` and
                       includes the `id` for recruiter responses.
- `AdminBase`: Base class for admin-related schemas,
               extending `UserBase`.
- `AdminCreate`: Inherits from `AdminBase` with
                the addition of `password` for creating an admin.
- `AdminResponse`: Inherits from `AdminBase` and
                   includes the `id` for admin responses.
- `DetailedInfoBase`: Base class for detailed information about a candidate.
- `DetailedInfoCreate`: Inherits from `DetailedInfoBase`
                        for creating detailed information records.
- `DetailedInfoResponse`: Inherits from `DetailedInfoBase` and
                          includes the `id` for detailed information responses.

Config Options:
- `from_attributes`: Automatically map attributes from the model during response generation.
- `extra='ignore'`: Ignore extra fields that are not
                    defined in the schema for the `DetailedInfoResponse` model.
"""

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict # Field

from app.models.model import UserRole


class UserBase(BaseModel):
    """
    Base class for defining user-related fields.

    Attributes:
        - `name`: Name of the user.
        - `email`: Email of the user.
    """
    name: str
    email: str


class UserCreate(UserBase):
    """
    Schema for creating a new user, including required attributes.

    Attributes:
        - `password`: Password for the user.
        - `role`: The role of the user in the system
                  (recruiter, admin, or candidate).
    """
    password: str
    role: UserRole


class UserResponse(UserBase):
    """
    Schema for responding with user data, including the `id`.

    Attributes:
        - `id`: Unique identifier for the user.
    """
    id: int

    class Config:
        from_attributes = True


class CandidateBase(UserBase):
    """
    Base schema for candidate-related fields.

    Attributes:
        - `applicationDate`: The date the candidate applied.
        - `applicationStatus`: Current status of the application.
    """
    applicationDate: datetime
    applicationStatus: str


class CandidateCreate(CandidateBase):
    """
    Schema for creating a candidate, including `user_id`.

    Attributes:
        - `user_id`: The ID of the associated user (foreign key).
    """
    user_id: int

    class Config:
        orm_mode = True


class CandidateResponse(CandidateBase):
    """
    Schema for responding with candidate data, including related user data.

    Attributes:
        - `id`: Unique identifier for the candidate.
        - `user`: Associated user data as a dictionary.
    """
    id: int
    user: dict

    class Config:
        from_attributes = True


class RecruiterBase(UserBase):
    """
    Base schema for recruiter-related fields.

    Attributes:
        - `user_id`: The ID of the associated user (foreign key).
    """
    user_id: int


class RecruiterCreate(RecruiterBase):
    """
    Schema for creating a recruiter, including password.

    Attributes:
        - `password`: Password for the recruiter.
    """
    password: str


class RecruiterResponse(RecruiterBase):
    """
    Schema for responding with recruiter data.

    Attributes:
        - `id`: Unique identifier for the recruiter.
    """
    id: int

    class Config:
        from_attributes = True


class AdminBase(UserBase):
    """
    Base schema for admin-related fields.
    """
    pass


class AdminCreate(AdminBase):
    """
    Schema for creating an admin, including password.

    Attributes:
        - `password`: Password for the admin.
    """
    password: str


class AdminResponse(AdminBase):
    """
    Schema for responding with admin data.

    Attributes:
        - `id`: Unique identifier for the admin.
    """
    id: int

    class Config:
        from_attributes = True

class DetailedInfoBase(BaseModel):
    """
    Base schema for detailed candidate information.

    Attributes:
        - Various fields related to the candidate's education,
           work experience, health, etc.
    """
    attending_school: Optional[str] = None
    level_of_schooling: Optional[str] = None
    fluent_english_scale: Optional[str] = None
    reading_english_scale: Optional[int] = None
    speaking_english_scale: Optional[int] = None
    writing_english_scale: Optional[int] = None
    numeracy_scale: Optional[int] = None
    computer_scale: Optional[int] = None
    work_experience: Optional[int] = None
    canada_work_ex: Optional[int] = None
    currently_employed: Optional[str] = None
    income_source: Optional[str] = None
    time_unemployed: Optional[int] = None
    substance_use: Optional[str] = None
    caregiver_bool: Optional[str] = None
    housing_bool: Optional[str] = None
    need_mental_health_support_bool: Optional[str] = None
    transportation_bool: Optional[str] = None
    felony_bool: Optional[str] = None

class DetailedInfoCreate(DetailedInfoBase):
    """
    Schema for creating detailed candidate information.
    """
    pass

class DetailedInfoResponse(DetailedInfoBase):
    """
    Schema for responding with detailed candidate information.

    Attributes:
        - `id`: Unique identifier for the detailed information record.
    """
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra='ignore'  # Ignore extra attributes not defined in the model
    )

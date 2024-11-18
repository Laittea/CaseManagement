from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from app.models.model import UserRole


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str
    role: UserRole


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class CandidateBase(UserBase):
    applicationDate: datetime
    applicationStatus: str


class CandidateCreate(CandidateBase):
    user_id: int

    class Config:
        orm_mode = True


class CandidateResponse(CandidateBase):
    id: int
    user: dict

    class Config:
        from_attributes = True


class RecruiterBase(UserBase):
    user_id: int


class RecruiterCreate(RecruiterBase):
    password: str


class RecruiterResponse(RecruiterBase):
    id: int

    class Config:
        from_attributes = True


class AdminBase(UserBase):
    pass


class AdminCreate(AdminBase):
    password: str


class AdminResponse(AdminBase):
    id: int

    class Config:
        from_attributes = True

class DetailedInfoBase(BaseModel):
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
    pass

class DetailedInfoResponse(DetailedInfoBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra='ignore'  # Ignore extra attributes not defined in the model
    )
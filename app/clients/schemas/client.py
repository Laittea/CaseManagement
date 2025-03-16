from pydantic import BaseModel, Field
from typing import Optional, List
from enum import IntEnum


class Gender(IntEnum):
    MALE = 1
    FEMALE = 2


class ClientBase(BaseModel):
    """Base schema for Client model"""

    age: int = Field(ge=18, description="Age of client, must be 18 or older")
    gender: Gender
    work_experience: int = Field(ge=0)
    canada_workex: int = Field(ge=0)
    dep_num: int = Field(ge=0)
    canada_born: bool
    citizen_status: bool
    level_of_schooling: int = Field(ge=1, le=14)
    fluent_english: bool
    reading_english_scale: int = Field(ge=0, le=10)
    speaking_english_scale: int = Field(ge=0, le=10)
    writing_english_scale: int = Field(ge=0, le=10)
    numeracy_scale: int = Field(ge=0, le=10)
    computer_scale: int = Field(ge=0, le=10)
    transportation_bool: bool
    caregiver_bool: bool
    housing: int = Field(ge=1, le=10)
    income_source: int = Field(ge=1, le=11)
    felony_bool: bool
    attending_school: bool
    currently_employed: bool
    substance_use: bool
    time_unemployed: int = Field(ge=0)
    need_mental_health_support_bool: bool


class ClientCreate(ClientBase):
    """Schema for creating a new client"""

    pass


class ClientUpdate(BaseModel):
    """Schema for updating an existing client"""

    age: Optional[int] = Field(None, ge=18)
    gender: Optional[Gender] = None
    work_experience: Optional[int] = Field(None, ge=0)
    canada_workex: Optional[int] = Field(None, ge=0)
    dep_num: Optional[int] = Field(None, ge=0)
    canada_born: Optional[bool] = None
    citizen_status: Optional[bool] = None
    level_of_schooling: Optional[int] = Field(None, ge=1, le=14)
    fluent_english: Optional[bool] = None
    reading_english_scale: Optional[int] = Field(None, ge=0, le=10)
    speaking_english_scale: Optional[int] = Field(None, ge=0, le=10)
    writing_english_scale: Optional[int] = Field(None, ge=0, le=10)
    numeracy_scale: Optional[int] = Field(None, ge=0, le=10)
    computer_scale: Optional[int] = Field(None, ge=0, le=10)
    transportation_bool: Optional[bool] = None
    caregiver_bool: Optional[bool] = None
    housing: Optional[int] = Field(None, ge=1, le=10)
    income_source: Optional[int] = Field(None, ge=1, le=11)
    felony_bool: Optional[bool] = None
    attending_school: Optional[bool] = None
    currently_employed: Optional[bool] = None
    substance_use: Optional[bool] = None
    time_unemployed: Optional[int] = Field(None, ge=0)
    need_mental_health_support_bool: Optional[bool] = None


class ClientResponse(ClientBase):
    """Schema for returning client details"""

    id: int

    class Config:
        from_attributes = True


class ClientListResponse(BaseModel):
    """Schema for returning multiple clients"""

    clients: List[ClientResponse]
    total: int

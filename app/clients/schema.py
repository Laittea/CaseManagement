"""
Schemas for client and prediction data models.
Defines Pydantic models for validation and data manipulation.
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel


class PredictionInput(BaseModel):
    """
    Schema for prediction input parameters.
    Used for validating data submitted for predictions.
    """
    age: int
    gender: str
    work_experience: int
    canada_workex: int
    dep_num: int
    canada_born: str
    citizen_status: str
    level_of_schooling: str
    fluent_english: str
    reading_english_scale: int
    speaking_english_scale: int
    writing_english_scale: int
    numeracy_scale: int
    computer_scale: int
    transportation_bool: str
    caregiver_bool: str
    housing: str
    income_source: str
    felony_bool: str
    attending_school: str
    currently_employed: str
    substance_use: str
    time_unemployed: int
    need_mental_health_support_bool: str


class Client(BaseModel):
    """
    Schema for client data.
    Represents information stored about a client in the database.
    """
    id: str
    first_name: str
    last_name: str
    email: str
    date_of_birth: date
    address: Optional[str] = None
    phone: Optional[str] = None


class ClientUpdate(BaseModel):
    """
    Schema for client update data.
    Used for partial updates to client information.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    phone: Optional[str] = None

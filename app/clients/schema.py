from pydantic import BaseModel
from typing import Optional
class PredictionInput(BaseModel):
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

# Pydantic Model for Request Body Validation
class ClientUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    work_experience: Optional[int] = None
    canada_workex: Optional[int] = None
    dep_num: Optional[int] = None
    canada_born: Optional[str] = None
    citizen_status: Optional[str] = None
    level_of_schooling: Optional[str] = None
    fluent_english: Optional[str] = None
    reading_english_scale: Optional[int] = None
    speaking_english_scale: Optional[int] = None
    writing_english_scale: Optional[int] = None
    numeracy_scale: Optional[int] = None
    computer_scale: Optional[int] = None
    transportation_bool: Optional[str] = None
    caregiver_bool: Optional[str] = None
    housing: Optional[str] = None
    income_source: Optional[str] = None
    felony_bool: Optional[str] = None
    attending_school: Optional[str] = None
    currently_employed: Optional[str] = None
    substance_use: Optional[str] = None
    time_unemployed: Optional[int] = None
    need_mental_health_support_bool: Optional[str] = None
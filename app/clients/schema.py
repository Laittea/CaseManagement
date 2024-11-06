from pydantic import BaseModel
from datetime import date
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

class Client(BaseModel):
    # ID will be auto-generated in a MangoDB database setup
    id: int  
    first_name: str
    last_name: str
    email: str
    date_of_birth: date
    address: Optional[str] = None
    phone: Optional[str] = None
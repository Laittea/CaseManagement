from pydantic import BaseModel, Field

class ClientUpdateModel(BaseModel):

    age: int = Field(None, example=30)
    gender: str = Field(None, example="Male")
    work_experience: int = Field(None, example=5)
    canada_workex: int = Field(None, example=2)
    dep_num: int = Field(None, example=1)
    canada_born: str = Field(None, example="No")
    citizen_status: str = Field(None, example="Citizen")
    level_of_schooling: str = Field(None, example="Bachelor’s degree")
    fluent_english: str = Field(None, example="Yes")
    reading_english_scale: int = Field(None, example=10)
    speaking_english_scale: int = Field(None, example=10)
    writing_english_scale: int = Field(None, example=10)
    numeracy_scale: int = Field(None, example=10)
    computer_scale: int = Field(None, example=10)
    transportation_bool: str = Field(None, example="No")
    caregiver_bool: str = Field(None, example="No")
    housing: str = Field(None, example="Renting")
    income_source: str = Field(None, example="Employment")
    felony_bool: str = Field(None, example="No")
    attending_school: str = Field(None, example="No")
    currently_employed: str = Field(None, example="Yes")
    substance_use: str = Field(None, example="No")
    time_unemployed: int = Field(None, example=0)
    need_mental_health_support_bool: str = Field(None, example="No")
    employment_assistance: int = Field(None, example=1)
    life_stabilization: int = Field(None, example=1)
    retention_services: int = Field(None, example=1)
    specialized_services: int = Field(None, example=1)
    employment_related_financial_supports: int = Field(None, example=1)
    employer_financial_supports: int = Field(None, example=1)
    enhanced_referrals: int = Field(None, example=1)
    success_rate: int = Field(None, example=100)

    class Config:
        orm_mode = True

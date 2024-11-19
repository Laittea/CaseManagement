from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

# Define the update request model based on actual Client model fields
class ClientUpdateRequest(BaseModel):
    age: Optional[int] = Field(None, description="Client's age")
    gender: Optional[bool] = Field(None, description="Client's gender")
    work_experience: Optional[int] = Field(None, description="Years of work experience")
    canada_workex: Optional[int] = Field(None, description="Years of work experience in Canada")
    dep_num: Optional[int] = Field(None, description="Number of dependents")
    canada_born: Optional[bool] = Field(None, description="Born in Canada")
    citizen_status: Optional[int] = Field(None, description="Citizen status")
    level_of_schooling: Optional[int] = Field(None, description="Highest level of schooling achieved")
    fluent_english: Optional[int] = Field(None, description="English fluency level")
    reading_english_scale: Optional[int] = Field(None, description="English reading scale")
    speaking_english_scale: Optional[int] = Field(None, description="English speaking comfort level")
    writing_english_scale: Optional[int] = Field(None, description="English writing scale")
    numeracy_scale: Optional[int] = Field(None, description="Numeracy scale")
    computer_scale: Optional[int] = Field(None, description="Computer use scale")
    transportation_bool: Optional[bool] = Field(None, description="Needs transportation support")
    caregiver_bool: Optional[bool] = Field(None, description="Is a primary caregiver")
    housing: Optional[int] = Field(None, description="Housing situation")
    income_source: Optional[int] = Field(None, description="Source of income")
    felony_bool: Optional[bool] = Field(None, description="Has a felony")
    attending_school: Optional[bool] = Field(None, description="Currently a student")
    currently_employed: Optional[bool] = Field(None, description="Currently employed")
    substance_use: Optional[bool] = Field(None, description="Substance use disorder")
    time_unemployed: Optional[int] = Field(None, description="Time unemployed")
    need_mental_health_support_bool: Optional[bool] = Field(None, description="Needs mental health support")

# Update client data in the database
def update_client_data(client_id: int, update_data: ClientUpdateRequest, db: Session):
    from .models import Client
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(client, key, value)

    db.commit()
    return client
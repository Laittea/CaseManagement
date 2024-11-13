# schema.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Common fields for all users
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

# Candidate schema
class CandidateBase(UserBase):
    applicationDate: datetime
    applicationStatus: str

class CandidateCreate(CandidateBase):
    user_id: int

class CandidateResponse(CandidateBase):
    id: int
    user: UserResponse

    class Config:
        from_attributes = True

# Recruiter schema
class RecruiterBase(UserBase):
    user_id: int

class RecruiterCreate(RecruiterBase):
    password: str

class RecruiterResponse(RecruiterBase):
    id: int

    class Config:
        from_attributes = True

# Admin schema
class AdminBase(UserBase):
    pass

class AdminCreate(AdminBase):
    password: str

class AdminResponse(AdminBase):
    id: int

    class Config:
        from_attributes = True

# DetailedInfo schema
class DetailedInfoBase(BaseModel):
    # Education-related attributes
    attendingSchool: Optional[str] = None
    levelOfSchooling: Optional[str] = None
    fluentEnglishScale: Optional[str] = None
    readingEnglishScale: Optional[int] = None
    speakingEnglishScale: Optional[int] = None
    writingEnglishScale: Optional[int] = None
    numeracyScale: Optional[int] = None
    computerScale: Optional[int] = None

    # Employment-related attributes
    workExperience: Optional[int] = None
    canadaWorkEx: Optional[int] = None
    currentlyEmployed: Optional[str] = None
    incomeSource: Optional[str] = None
    timeUnemployed: Optional[int] = None
    substance_use: Optional[str] = None

    # Support needs-related attributes
    caregiverBool: Optional[str] = None
    housingBool: Optional[str] = None
    needMentalHealthSupportBool: Optional[str] = None
    transportationBool: Optional[str] = None

    # Criminal history-related attribute
    felonyBool: Optional[str] = None

class DetailedInfoCreate(DetailedInfoBase):
    pass

class DetailedInfoResponse(DetailedInfoBase):
    id: int

    class Config:
        from_attributes = True

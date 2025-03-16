from pydantic import BaseModel, Field, validator
from app.models import UserRole


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str
    role: UserRole

    @validator("role")
    def validate_role(cls, v):
        if v not in [UserRole.admin, UserRole.case_worker]:
            raise ValueError("Role must be either admin or case_worker")
        return v


class UserResponse(BaseModel):
    username: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True

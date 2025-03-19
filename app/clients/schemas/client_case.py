from pydantic import BaseModel, Field
from typing import Optional


class ClientCaseBase(BaseModel):
    """Base schema for ClientCase used for API validation."""

    client_id: int
    user_id: int
    employment_assistance: bool
    life_stabilization: bool
    retention_services: bool
    specialized_services: bool
    employment_related_financial_supports: bool
    employer_financial_supports: bool
    enhanced_referrals: bool
    success_rate: int = Field(ge=0, le=100)


class ClientCaseCreate(ClientCaseBase):
    """Schema for creating a client case."""

    pass


class ClientCaseUpdate(BaseModel):
    """Schema for updating client case information."""

    employment_assistance: Optional[bool] = None
    life_stabilization: Optional[bool] = None
    retention_services: Optional[bool] = None
    specialized_services: Optional[bool] = None
    employment_related_financial_supports: Optional[bool] = None
    employer_financial_supports: Optional[bool] = None
    enhanced_referrals: Optional[bool] = None
    success_rate: Optional[int] = Field(None, ge=0, le=100)


class ClientCaseResponse(ClientCaseBase):
    """Schema for returning client case details."""

    class Config:
        from_attributes = True


class ServiceUpdate(BaseModel):
    """Schema for updating client services."""

    employment_assistance: Optional[bool] = None
    life_stabilization: Optional[bool] = None
    retention_services: Optional[bool] = None
    specialized_services: Optional[bool] = None
    employment_related_financial_supports: Optional[bool] = None
    employer_financial_supports: Optional[bool] = None
    enhanced_referrals: Optional[bool] = None
    success_rate: Optional[int] = Field(None, ge=0, le=100)


class ServiceResponse(BaseModel):
    """Schema for returning client service details"""

    client_id: int
    user_id: int
    employment_assistance: bool
    life_stabilization: bool
    retention_services: bool
    specialized_services: bool
    employment_related_financial_supports: bool
    employer_financial_supports: bool
    enhanced_referrals: bool
    success_rate: int = Field(ge=0, le=100)

    class Config:
        from_attributes = True

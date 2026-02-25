from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LocationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Location name / area name")
    address: Optional[str] = Field(None, max_length=255, description="Street address")
    city: str = Field(..., min_length=2, max_length=100, description="City")
    state: Optional[str] = Field(None, max_length=100, description="State")
    pincode: Optional[str] = Field(None, max_length=20, description="PIN / ZIP code")


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None


class LocationResponse(LocationBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

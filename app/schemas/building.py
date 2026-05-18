from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BuildingBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Building name")
    location_id: int = Field(..., description="ID of the location this building belongs to")
    address: Optional[str] = Field(None, max_length=255, description="Building street address")
    total_floors: int = Field(default=1, ge=1, description="Total number of floors")
    description: Optional[str] = Field(None, description="Additional description")


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    total_floors: Optional[int] = Field(None, ge=1)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class BuildingResponse(BuildingBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


VALID_ROOM_TYPES = ["single", "double", "triple", "pg"]
VALID_STATUSES = ["vacant", "occupied", "maintenance"]


class RoomBase(BaseModel):
    room_number: str = Field(..., min_length=1, max_length=20, description="Room number e.g. 101, A-12")
    building_id: int = Field(..., description="ID of the building this room belongs to")
    floor: int = Field(default=1, ge=0, description="Floor number (0 = ground floor)")
    room_type: str = Field(default="single", description="single / double / triple / pg")
    capacity: int = Field(default=1, ge=1, description="Max number of tenants")
    rent_amount: float = Field(..., gt=0, description="Monthly rent amount")
    amenities: Optional[str] = Field(None, description="Comma-separated amenities e.g. AC, WiFi, Geyser")
    description: Optional[str] = Field(None, description="Additional description")

    @field_validator("room_type")
    @classmethod
    def validate_room_type(cls, v):
        if v not in VALID_ROOM_TYPES:
            raise ValueError(f"room_type must be one of {VALID_ROOM_TYPES}")
        return v


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    room_number: Optional[str] = Field(None, min_length=1, max_length=20)
    floor: Optional[int] = Field(None, ge=0)
    room_type: Optional[str] = None
    capacity: Optional[int] = Field(None, ge=1)
    rent_amount: Optional[float] = Field(None, gt=0)
    status: Optional[str] = None
    amenities: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("room_type")
    @classmethod
    def validate_room_type(cls, v):
        if v is not None and v not in VALID_ROOM_TYPES:
            raise ValueError(f"room_type must be one of {VALID_ROOM_TYPES}")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}")
        return v


class RoomResponse(RoomBase):
    id: int
    status: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

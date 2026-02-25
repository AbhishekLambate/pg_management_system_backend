from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
from datetime import datetime, date


VALID_STATUSES = ["active", "checked_out", "on_notice"]
VALID_ID_PROOFS = ["aadhar", "passport", "driving_license", "voter_id", "other"]


class TenantCreate(BaseModel):
    # Personal info
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    alternate_phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    permanent_address: Optional[str] = None

    # Emergency contact
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)

    # ID proof
    id_proof_type: Optional[str] = None
    id_proof_number: Optional[str] = Field(None, max_length=50)

    # Stay details
    room_id: Optional[int] = None
    move_in_date: Optional[date] = None
    deposit_amount: float = Field(default=0.0, ge=0)

    # Optional: create a login account for this tenant
    create_login: bool = Field(default=False, description="Set true to create a user login account")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Required if create_login=True")
    password: Optional[str] = Field(None, min_length=6, description="Required if create_login=True")

    @field_validator("id_proof_type")
    @classmethod
    def validate_id_proof(cls, v):
        if v is not None and v not in VALID_ID_PROOFS:
            raise ValueError(f"id_proof_type must be one of {VALID_ID_PROOFS}")
        return v


class TenantUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    alternate_phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    permanent_address: Optional[str] = None
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    id_proof_type: Optional[str] = None
    id_proof_number: Optional[str] = Field(None, max_length=50)
    deposit_amount: Optional[float] = Field(None, ge=0)
    status: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}")
        return v


class AssignRoomSchema(BaseModel):
    room_id: int = Field(..., description="ID of the room to assign")
    move_in_date: Optional[date] = None


class CheckoutSchema(BaseModel):
    move_out_date: date = Field(..., description="Date of checkout")


class TenantResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    room_id: Optional[int] = None
    first_name: str
    last_name: str
    phone: str
    alternate_phone: Optional[str] = None
    email: Optional[str] = None
    permanent_address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    id_proof_type: Optional[str] = None
    id_proof_number: Optional[str] = None
    move_in_date: Optional[date] = None
    move_out_date: Optional[date] = None
    deposit_amount: float
    status: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

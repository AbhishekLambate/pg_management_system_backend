from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StaffBase(BaseModel):
    name: str
    role: str
    phone: str
    location: str
    status: Optional[str] = "Active"

class StaffCreate(StaffBase): pass
class StaffUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None

class StaffResponse(StaffBase):
    id: int
    created_at: datetime
    class Config: from_attributes = True

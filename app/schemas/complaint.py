from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ComplaintBase(BaseModel):
    title: str
    tenant_id: int
    status: Optional[str] = "Pending"
    priority: Optional[str] = "Medium"

class ComplaintCreate(ComplaintBase): pass
class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None

class ComplaintResponse(ComplaintBase):
    id: int
    ticket_id: Optional[str] = None
    created_at: datetime
    tenant_name: Optional[str] = None
    class Config: from_attributes = True

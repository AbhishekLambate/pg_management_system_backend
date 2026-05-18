from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VisitorBase(BaseModel):
    name: str
    tenant_id: int
    relation: Optional[str] = None
    in_time: Optional[datetime] = None
    out_time: Optional[datetime] = None

class VisitorCreate(VisitorBase): pass

class VisitorResponse(VisitorBase):
    id: int
    created_at: datetime
    tenant_name: Optional[str] = None
    class Config: from_attributes = True

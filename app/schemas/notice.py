from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoticeBase(BaseModel):
    title: str
    content: str
    type: Optional[str] = "Info"

class NoticeCreate(NoticeBase): pass

class NoticeResponse(NoticeBase):
    id: int
    created_at: datetime
    class Config: from_attributes = True

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    tenant_id: int
    amount: float
    payment_date: Optional[datetime] = None
    month: str = Field(..., max_length=50)
    status: str = Field(default="pending", max_length=20)
    payment_mode: Optional[str] = Field(None, max_length=50)
    reference_id: Optional[str] = Field(None, max_length=100)

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_date: Optional[datetime] = None
    month: Optional[str] = None
    status: Optional[str] = None
    payment_mode: Optional[str] = None
    reference_id: Optional[str] = None

class PaymentResponse(PaymentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    tenant_name: Optional[str] = None

    class Config:
        from_attributes = True

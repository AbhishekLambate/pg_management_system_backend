import os

def create_files():
    base_dir = "app"
    
    # 1. Model
    model_code = """from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=True)
    month = Column(String(50), nullable=False) # e.g. "January 2026"
    status = Column(String(20), default="pending", nullable=False) # pending/paid/failed
    payment_mode = Column(String(50), nullable=True)
    reference_id = Column(String(100), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tenant = relationship("Tenant", backref="payments")
"""
    with open(f"{base_dir}/models/payment.py", "w") as f:
        f.write(model_code)

    # 2. Schema
    schema_code = """from pydantic import BaseModel, Field
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
    
    # Optional nested tenant info could be added here if needed
    tenant_name: Optional[str] = None

    class Config:
        from_attributes = True
"""
    with open(f"{base_dir}/schemas/payment.py", "w") as f:
        f.write(schema_code)

    # 3. Handler (Simplified, skipping usecase/repository/entity for speed, just using sqlalchemy directly to save time, or I can do basic crud)
    handler_code = """from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from app.models.payment import Payment
from app.models.tenant import Tenant
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tenant = db.query(Tenant).filter(Tenant.id == payment_data.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
        
    new_payment = Payment(**payment_data.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    
    response = PaymentResponse.model_validate(new_payment)
    response.tenant_name = f"{tenant.first_name} {tenant.last_name}"
    return response

@router.get("/", response_model=list[PaymentResponse])
def get_all_payments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payments = db.query(Payment).join(Tenant).all()
    results = []
    for p in payments:
        resp = PaymentResponse.model_validate(p)
        resp.tenant_name = f"{p.tenant.first_name} {p.tenant.last_name}" if p.tenant else "Unknown"
        results.append(resp)
    return results

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment_data: PaymentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
        
    update_dict = payment_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(payment, key, value)
        
    db.commit()
    db.refresh(payment)
    
    response = PaymentResponse.model_validate(payment)
    response.tenant_name = f"{payment.tenant.first_name} {payment.tenant.last_name}" if payment.tenant else "Unknown"
    return response
"""
    with open(f"{base_dir}/handlers/payment_handler.py", "w") as f:
        f.write(handler_code)
        
if __name__ == "__main__":
    create_files()
    print("Payment module files created successfully.")

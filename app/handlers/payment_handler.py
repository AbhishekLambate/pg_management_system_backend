from fastapi import APIRouter, Depends, HTTPException, status
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

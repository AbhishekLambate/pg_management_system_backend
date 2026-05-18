from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate, ComplaintResponse
from app.models.complaint import Complaint
from app.models.tenant import Tenant
import uuid

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])

@router.get("/", response_model=list[ComplaintResponse])
def get_complaints(db: Session = Depends(get_db)):
    complaints = db.query(Complaint).all()
    results = []
    for c in complaints:
        resp = ComplaintResponse.model_validate(c)
        resp.tenant_name = f"{c.tenant.first_name} {c.tenant.last_name}" if c.tenant else "Unknown"
        results.append(resp)
    return results

@router.post("/", response_model=ComplaintResponse)
def create_complaint(data: ComplaintCreate, db: Session = Depends(get_db)):
    obj = Complaint(**data.model_dump())
    obj.ticket_id = f"TKT-{str(uuid.uuid4())[:8].upper()}"
    db.add(obj)
    db.commit()
    db.refresh(obj)
    resp = ComplaintResponse.model_validate(obj)
    return resp

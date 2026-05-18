from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.staff import StaffCreate, StaffUpdate, StaffResponse
from app.models.staff import Staff

router = APIRouter(prefix="/api/staff", tags=["Staff"])

@router.get("/", response_model=list[StaffResponse])
def get_staff(db: Session = Depends(get_db)):
    return db.query(Staff).all()

@router.post("/", response_model=StaffResponse)
def create_staff(data: StaffCreate, db: Session = Depends(get_db)):
    obj = Staff(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

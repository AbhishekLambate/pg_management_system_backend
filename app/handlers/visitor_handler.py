from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.visitor import VisitorCreate, VisitorResponse
from app.models.visitor import Visitor

router = APIRouter(prefix="/api/visitors", tags=["Visitors"])

@router.get("/", response_model=list[VisitorResponse])
def get_visitors(db: Session = Depends(get_db)):
    visitors = db.query(Visitor).all()
    results = []
    for v in visitors:
        resp = VisitorResponse.model_validate(v)
        resp.tenant_name = f"{v.tenant.first_name} {v.tenant.last_name}" if v.tenant else "Unknown"
        results.append(resp)
    return results

@router.post("/", response_model=VisitorResponse)
def create_visitor(data: VisitorCreate, db: Session = Depends(get_db)):
    obj = Visitor(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return VisitorResponse.model_validate(obj)

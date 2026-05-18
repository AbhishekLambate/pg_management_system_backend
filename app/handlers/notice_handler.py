from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.notice import NoticeCreate, NoticeResponse
from app.models.notice import Notice

router = APIRouter(prefix="/api/notices", tags=["Notices"])

@router.get("/", response_model=list[NoticeResponse])
def get_notices(db: Session = Depends(get_db)):
    return db.query(Notice).order_by(Notice.created_at.desc()).all()

@router.post("/", response_model=NoticeResponse)
def create_notice(data: NoticeCreate, db: Session = Depends(get_db)):
    obj = Notice(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

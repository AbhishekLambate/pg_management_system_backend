import os

base_dir = "/home/ubuntu/Documents/Abhi_Important/pg-management/pg_management_system_backend/app"

modules = {
    "staff": {
        "model": """from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    location = Column(String(100), nullable=False)
    status = Column(String(20), default="Active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
""",
        "schema": """from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StaffBase(BaseModel):
    name: str
    role: str
    phone: str
    location: str
    status: Optional[str] = "Active"

class StaffCreate(StaffBase): pass
class StaffUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None

class StaffResponse(StaffBase):
    id: int
    created_at: datetime
    class Config: from_attributes = True
""",
        "handler": """from fastapi import APIRouter, Depends, HTTPException
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
"""
    },
    "complaint": {
        "model": """from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String(50), unique=True, index=True)
    title = Column(String(200), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="Pending")
    priority = Column(String(50), default="Medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    tenant = relationship("Tenant", backref="complaints")
""",
        "schema": """from pydantic import BaseModel
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
""",
        "handler": """from fastapi import APIRouter, Depends, HTTPException
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
"""
    },
    "expense": {
        "model": """from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    expense_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
""",
        "schema": """from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExpenseBase(BaseModel):
    title: str
    amount: float
    category: str
    expense_date: Optional[datetime] = None

class ExpenseCreate(ExpenseBase): pass

class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime
    class Config: from_attributes = True
""",
        "handler": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.models.expense import Expense

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])

@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()

@router.post("/", response_model=ExpenseResponse)
def create_expense(data: ExpenseCreate, db: Session = Depends(get_db)):
    obj = Expense(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
"""
    },
    "visitor": {
        "model": """from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Visitor(Base):
    __tablename__ = "visitors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    relation = Column(String(100), nullable=True)
    in_time = Column(DateTime(timezone=True), nullable=True)
    out_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tenant = relationship("Tenant", backref="visitors")
""",
        "schema": """from pydantic import BaseModel
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
""",
        "handler": """from fastapi import APIRouter, Depends
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
"""
    },
    "notice": {
        "model": """from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Notice(Base):
    __tablename__ = "notices"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String(50), default="Info")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
""",
        "schema": """from pydantic import BaseModel
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
""",
        "handler": """from fastapi import APIRouter, Depends
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
"""
    }
}

for mod, files in modules.items():
    with open(os.path.join(base_dir, f"models/{mod}.py"), "w") as f:
        f.write(files["model"])
    with open(os.path.join(base_dir, f"schemas/{mod}.py"), "w") as f:
        f.write(files["schema"])
    with open(os.path.join(base_dir, f"handlers/{mod}_handler.py"), "w") as f:
        f.write(files["handler"])

print("Successfully scaffolded 5 new backend modules.")

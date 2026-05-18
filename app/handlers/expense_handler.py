from fastapi import APIRouter, Depends
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

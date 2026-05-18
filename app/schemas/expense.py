from pydantic import BaseModel
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

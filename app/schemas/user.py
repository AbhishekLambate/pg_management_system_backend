from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: str = Field(default="user")  # 'admin' or 'user', default is 'user'
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        """Validate role is either 'admin' or 'user'."""
        if v not in ["admin", "user"]:
            raise ValueError("Role must be either 'admin' or 'user'")
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
    
    @property
    def is_admin(self) -> bool:
        """Check if user is admin based on role."""
        return self.role == "admin"


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


from datetime import datetime
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

class UserCreate(BaseModel):
    nickname: str
    email: EmailStr
    password: str

    @validator('password')
    def password_complexity(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search("[a-z]", v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search("[A-Z]", v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search("[0-9]", v):
            raise ValueError('Password must contain at least one digit')
        if not re.search("[@#$%^&+=]", v):
            raise ValueError('Password must contain at least one special character')
        return v

class User(BaseModel):
    id: int
    nickname: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

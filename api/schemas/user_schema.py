from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    
class UserUpdate(BaseModel):
    email: str = None
    password: str = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    score: int

    class Config:
        orm_mode:True

class AttemptResponse(BaseModel):
    id: int
    problem_title: str
    passed: bool
    created_at: datetime

    class Config:
        orm_mode = True

class ProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    score: int
    attempts: List[AttemptResponse]
    
    class Config:
        orm_mode: True
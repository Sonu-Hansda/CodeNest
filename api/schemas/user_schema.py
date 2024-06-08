from pydantic import BaseModel, EmailStr

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

    class Config:
        orm_mode:True
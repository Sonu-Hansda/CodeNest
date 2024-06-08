from jose import jwt
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import User
from database import get_db
from schemas import UserCreate,UserResponse, UserUpdate, Token, UserLogin
from utils import create_access_token, verify_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Get all users
@router.get("/getAll",response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if users is None:
        return []
    return users

# Get one user my Id
@router.get("/{user_Id}",response_model=UserResponse)
def get_user(user_Id: int, db: Session = (Depends(get_db))):
    user = db.query(User).filter(User.id == user_Id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id: {user_Id} not found")
    return user

# Create a new user
@router.post("/register",response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        new_user = User(user.username, user.email, user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        access_token = create_access_token({"sub":new_user.email})
        return {"access_token":access_token, "token_type":"bearer"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"error : {err}")

# Login user
@router.post("/login", response_model=Token)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not user.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Update User data
@router.put("/{user_Id}",response_model=UserResponse)
def update_user(user_Id: int, user:UserUpdate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_Id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key,value in user.model_dump().items():
        setattr(existing_user,key,value)
    db.commit()
    db.refresh(existing_user)
    return existing_user

# Patch User data
@router.patch("/{user_Id}",response_model=UserResponse)
def update_user(user_Id: int, user:UserUpdate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_Id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key,value in user.model_dump().items():
        setattr(existing_user,key,value)
    db.commit()
    db.refresh(existing_user)
    return existing_user

# Delete User
@router.delete("/{user_Id}",response_model=UserResponse)
def delete_user(user_Id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_Id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_Id} does not exists")
    db.delete(user)
    db.commit()
    return user

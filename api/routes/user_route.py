from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Attempt
from database import get_db
from schemas import UserCreate,UserResponse, UserUpdate, Token, UserLogin, ProfileResponse, TokenData, AttemptResponse
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()


ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "8dd3831e4cc328c3c3da6b9fde4d3495fac1cb450aa62512d9469dab1f481bcd"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@router.get("/profile", response_model=ProfileResponse)
def get_profile(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    recent_attempts = (
        db.query(Attempt)
        .filter(Attempt.user_id == user.id)
        .order_by(Attempt.created_at.desc())
        .limit(10)
        .all()
    )
    attempts_data = [
        AttemptResponse(
            id=attempt.id,
            problem_title=attempt.problem.title,
            passed=attempt.passed,
            created_at=attempt.created_at,
        )
        for attempt in recent_attempts
    ]
    return ProfileResponse(id=user.id,username=user.username,email=user.email,score=user.score,attempts=[i for i in attempts_data])

# Create a new user
@router.post("/register",response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        print("fine")
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


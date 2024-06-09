from fastapi import FastAPI, Depends
from typing import List
from schemas import UserResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi.middleware.cors import CORSMiddleware
from routes import UserRouter, ProblemRouter
from database import Base, engine, get_db
from models import User

Base.metadata.create_all(bind=engine)
app = FastAPI()

# CORS middleware to allow requests from frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get leaderboard
@app.get("/api/leaderboard",response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(desc(User.score)).all()
    if users is None:
        return []
    return users
app.include_router(UserRouter,prefix="/api/account")
app.include_router(ProblemRouter,prefix="/api/problems")
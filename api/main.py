from jose import JWTError
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import UserRouter, ProblemRouter
from database import Base, engine, get_db
from models import User, Problem
from schemas import Token
from sqlalchemy.orm import Session
from utils import create_access_token,verify_access_token

app = FastAPI()
Base.metadata.create_all(bind=engine)

# CORS middleware to allow requests from frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT token validation middleware
async def jwt_authentication(request: Request):
    try:
        token = request.headers["Authorization"].split("Bearer ")[1]
        payload = verify_access_token(token)
        # Add user data to request state for use in route handlers
        request.state.user = payload
    except (KeyError, JWTError, IndexError):
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )
    return request

@app.get("/protected")
def protected(request: Request = Depends(jwt_authentication)):
    user = request.state.user
    return {"message":"This is a protected endpoint","user":user}

app.include_router(UserRouter,prefix="/api/account")
app.include_router(ProblemRouter,prefix="/api/problems")
from sqlalchemy import Column, Integer, String, DateTime
from utils import GenUniqueID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,index=True)
    email = Column(String,unique=True,index=True)
    hashed_password = Column(String)
    score = Column(Integer, default=0)
    problems = relationship("Problem",back_populates="author")
    attempts = relationship("Attempt", back_populates="user")
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.hashed_password = self.hash_password(password)
        self.id = self.set_id()

    def set_id(self):
        return GenUniqueID()

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password,hashed_password):
        return pwd_context.verify(plain_password,hashed_password)
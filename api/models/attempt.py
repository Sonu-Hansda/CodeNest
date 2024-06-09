from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from utils import GenUniqueID
from database import Base

class Attempt(Base):
    __tablename__ = 'attempts'

    id = Column(Integer, primary_key=True, index=True , unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    problem_id = Column(Integer, ForeignKey('problems.id'))
    passed = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="attempts")
    problem = relationship("Problem", back_populates="attempts")
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, user_id, problem_id, passed):
        self.user_id = user_id
        self.problem_id = problem_id
        self.passed = passed
        self.id = self.set_id()
    
    def set_id(self):
       return GenUniqueID()
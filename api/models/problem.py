from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from utils import GenUniqueID
from database import Base

class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer,primary_key=True,unique=True, index=True)
    title = Column(Text,unique=True,nullable=False,index=True)
    description = Column(Text, nullable=False)
    code = Column(Text,nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates='problems')
    test_cases = relationship("TestCase",back_populates="problem",cascade="all, delete-orphan")

    def __init__(self,title,description,code,author_id):
        self.title = title
        self.description = description
        self.code = code
        self.author_id = author_id
        self.id = self.set_id()
    
    def set_id(self):
       return GenUniqueID()

class TestCase(Base):
    __tablename__ = 'test_cases'

    id = Column(Integer, primary_key=True, index=True , unique=True)
    input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    problem_id = Column(Integer, ForeignKey('problems.id'))
    problem = relationship("Problem",back_populates='test_cases')

    def __init__(self,input,expected_output,problem_id):
        self.input = input
        self.expected_output = expected_output
        self.problem_id = problem_id

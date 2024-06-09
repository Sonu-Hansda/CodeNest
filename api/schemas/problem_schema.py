from pydantic import BaseModel, Field
from typing import List, Optional
from .user_schema import UserResponse

class SolutionCreate(BaseModel):
    problem_code: int
    language: str
    code: str

class TestCaseResult(BaseModel):
    input: str
    expected_output: str
    actual_output: str
    error_output: Optional[str]
    passed: bool
    time_taken: Optional[float] = Field(None, description="Time taken to execute in seconds")

class EvaluationResult(BaseModel):
    test_cases: List[TestCaseResult]

class TestCaseCreate(BaseModel):
    input: str
    expected_output: str

class ProblemCreate(BaseModel):
    title: str
    description: str
    code: str
    point: int
    test_cases: List[TestCaseCreate] = Field(default_factory=list)

class ProblemResponse(BaseModel):
    id: int
    title: str
    description: str
    author: UserResponse
    code: str
    test_cases: List[TestCaseCreate]

    class Config:
        orm_mode: True
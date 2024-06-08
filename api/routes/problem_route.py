from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Problem, TestCase
from database import get_db
from schemas import ProblemCreate, ProblemResponse, EvaluationResult, SolutionCreate, TestCaseResult
from utils import PY_Eval, C_Eval, CPP_Eval

router = APIRouter()

# Get All Problem statements
@router.get("/getAll",response_model=List[ProblemResponse])
def get_all_problem_statements(db: Session = Depends(get_db)):
    db_problems = db.query(Problem).all()
    if db_problems is None:
        return []
    return db_problems

# Create problem statement
@router.post("/",response_model=ProblemResponse)
def create_problem_statement(problem:ProblemCreate, db: Session = Depends(get_db)):
    db_problem = db.query(Problem).filter(Problem.title == problem.title).first()
    if db_problem is not None:
        raise HTTPException(status_code=403, detail="Problem statement already exists")
    try:
        new_problem = Problem(problem.title,problem.description,problem.code,problem.author_id)
        db.add(new_problem)
        db.commit()
        db.refresh(new_problem)

        for tc in problem.test_cases:
            new_test_cases = TestCase(
                input=tc.input,
                expected_output=tc.expected_output,
                problem_id= new_problem.id
            )

            db.add(new_test_cases)
        
        db.commit()
        db.refresh(new_problem)
        return new_problem
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"error: {err}")

# Submit solution
@router.post("/evaluate")
def evaluate_solution(solution: SolutionCreate, db: Session = Depends(get_db)):
    p_statement = db.query(Problem).filter(Problem.id == solution.problem_code).first()
    if p_statement is None:
        raise HTTPException(status_code=404, detail="Problem statement not found")
    
    test_cases = [{"input":tc.input,"expected_output":tc.expected_output} for tc in p_statement.test_cases]
    match solution.language:
        case "python":
            result = PY_Eval.evaluate_code(solution.code,test_cases)
        case "c":
            result = C_Eval.evaluate_code(solution.code, test_cases)
        case "cpp":
            result = CPP_Eval.evaluate_code(solution.code, test_cases)
        
    return EvaluationResult(test_cases=result)


# Delete Problem Statement
@router.delete("/{p_Id}",response_model=ProblemResponse)
def delete_user(p_Id: int, db: Session = Depends(get_db)):
    p_statement = db.query(Problem).filter(Problem.id == p_Id).first()
    if p_statement is None:
        raise HTTPException(status_code=404, detail=f"Problem statement not found")
    db.delete(p_statement)
    db.commit()
    return p_statement
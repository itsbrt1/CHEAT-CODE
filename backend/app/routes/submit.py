from fastapi import APIRouter
from pydantic import BaseModel
from app.services.judge import judge_submission, get_problems, get_history

router = APIRouter()

class Submission(BaseModel):
    code: str
    problem_id: int

@router.get("/problems")
def problems():
    return get_problems()

@router.post("/submit")
def submit(submission: Submission):
    return judge_submission(submission.problem_id, submission.code)

@router.get("/history")
def history():
    return get_history()
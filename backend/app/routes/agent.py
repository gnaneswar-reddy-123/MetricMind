from fastapi import APIRouter, Query
from app.services.agent_service import analyze_question

router = APIRouter(
    prefix="/api/agent",
    tags=["Agent"]
)


@router.get("/ask")
def ask_question(
    question: str = Query(...)
):
    return analyze_question(question)
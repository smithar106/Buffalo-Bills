"""Chat endpoint — the agent API."""

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.agent import run

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    question: str
    mode: Optional[str] = "bills_mafia"
    context: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    mode: str
    sources: list
    demo: bool
    fallback: bool
    tool_calls: list
    validation: dict


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = run(req.question, req.mode, req.context)
    return ChatResponse(
        answer=result["answer"],
        mode=result["mode"],
        sources=result["sources"],
        demo=result["demo"],
        fallback=result["fallback"],
        tool_calls=result["tool_calls"],
        validation=result["validation"],
    )

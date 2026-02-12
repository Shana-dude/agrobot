from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from .rag_pipeline import answer_question
from .database import save_chat, get_recent_chats

router = APIRouter()

class Question(BaseModel):
    query: str
    lat: Optional[float] = None
    lon: Optional[float] = None

@router.post("/api/tomato-chat")
async def chat(question: Question):
    response = answer_question(question.query, lat=question.lat, lon=question.lon)
    # Save to MongoDB asynchronously
    await save_chat(question.query, response)
    return {"answer": response}

@router.get("/api/history")
async def history():
    chats = await get_recent_chats()
    return {"history": chats}

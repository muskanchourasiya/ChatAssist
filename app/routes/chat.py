from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag import rag_pipeline

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
def chat(req: ChatRequest):
    answer = rag_pipeline(req.query)
    return {"answer": answer}
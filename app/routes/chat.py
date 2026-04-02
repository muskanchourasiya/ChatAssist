from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import uuid
import logging

from app.services.rag import rag_pipeline, retrieve, build_prompt
from app.services.memory import add_message, get_history
from app.services.guardrails import validate_input, detect_prompt_injection, filter_pii
from app.services.llm import stream_answer

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    role: str
    session_id: str | None = None


@router.post("/chat")
def chat(req: ChatRequest):
    validate_input(req.query)
    detect_prompt_injection(req.query)

    session_id = req.session_id or str(uuid.uuid4())
    history = get_history(session_id)

    result = rag_pipeline(req.query, history, req.role)

    answer = filter_pii(result["answer"])

    add_message(session_id, "user", req.query)
    add_message(session_id, "assistant", answer)

    return {
        "answer": answer,
        "sources": result["sources"],
        "session_id": session_id
    }


@router.post("/chat/stream")
def chat_stream(req: ChatRequest):
    logging.info(f"Query: {req.query}")
    logging.info(f"Role: {req.role}")
    logging.info(f"Session ID: {req.session_id}")

    history = get_history(req.session_id or "default")
    docs = retrieve(req.query)
    prompt = build_prompt(req.query, docs, history)

    def generate():
        for token in stream_answer(prompt):
            yield token

    return StreamingResponse(generate(), media_type="text/plain")
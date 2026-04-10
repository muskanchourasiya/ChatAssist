from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import uuid
import logging

from app.services.memory import add_message, get_history
from app.services.guardrails import validate_input, detect_prompt_injection, filter_pii
from app.graph.graph_builder import build_graph

router = APIRouter()

graph = build_graph()

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

    state = {
        "query": req.query,
        "role": req.role,
        "history": history,
        "docs": [],
        "prompt": "",
        "answer": "",
        "sources": []
    }

    result = graph.invoke(state)

    answer = filter_pii(result["answer"])

    add_message(session_id, "user", req.query)
    add_message(session_id, "assistant", answer)

    return {
        "answer": answer,
        "sources": result.get("sources", []),
        "session_id": session_id
    }

@router.post("/chat/stream")
def chat_stream(req: ChatRequest):

    validate_input(req.query)
    detect_prompt_injection(req.query)

    session_id = req.session_id or str(uuid.uuid4())
    history = get_history(session_id)

    state = {
        "query": req.query,
        "role": req.role,
        "history": history,
        "docs": [],
        "prompt": "",
        "answer": "",
        "sources": []
    }

    def generate():

        final_state = None

        for step in graph.stream(state):
            final_state = step

            if "answer" in step:
                yield step["answer"]

        if final_state and "answer" in final_state:
            answer = filter_pii(final_state["answer"])
            add_message(session_id, "user", req.query)
            add_message(session_id, "assistant", answer)

    return StreamingResponse(generate(), media_type="text/plain")
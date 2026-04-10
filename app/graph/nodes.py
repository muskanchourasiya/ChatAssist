from app.services.guardrails import validate_input, detect_prompt_injection
from app.services.rag import retrieve
from app.services.rag import build_prompt
from app.services.llm import generate_answer

def guardrails_node(state):
    validate_input(state["query"])
    detect_prompt_injection(state["query"])
    return state

def retrieve_node(state):

    result = retrieve(state["query"], state["role"])

    state["docs"] = result["documents"]

    return state

def prompt_node(state):

    prompt = build_prompt(
        state["query"],
        state["docs"],
        state["history"]
    )

    state["prompt"] = prompt

    return state

def llm_node(state):

    answer = generate_answer(state["prompt"])

    state["answer"] = answer

    return state
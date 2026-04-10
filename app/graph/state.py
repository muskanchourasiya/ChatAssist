from typing import TypedDict, List

class GraphState(TypedDict):

    query: str
    role: str
    history: List

    docs: List
    prompt: str

    answer: str
    sources: List
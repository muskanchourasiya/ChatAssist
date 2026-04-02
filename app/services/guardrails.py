import re

def validate_input(query: str):
    if len(query) > 500:
        raise ValueError("Query too long")

def detect_prompt_injection(query: str):
    suspicious = ["ignore previous", "system prompt", "bypass"]

    for word in suspicious:
        if word in query.lower():
            raise ValueError("Prompt injection detected")

def filter_pii(text: str):
    return re.sub(r"\S+@\S+", "[EMAIL_MASKED]", text)
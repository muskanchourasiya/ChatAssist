from fastapi import FastAPI
from app.routes import chat, upload

app = FastAPI()

app.include_router(chat.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
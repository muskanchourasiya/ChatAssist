from fastapi import FastAPI
from app.routes import chat, upload
import logging

app = FastAPI()

app.include_router(chat.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
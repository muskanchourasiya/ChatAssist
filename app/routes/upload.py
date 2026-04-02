from fastapi import APIRouter, UploadFile
import os
from app.utils.parser import extract_text_from_pdf
from app.utils.chunking import chunk_text
from app.services.embeddings import get_embedding
from app.db.chroma import collection
import uuid

router = APIRouter()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)

    ids = []
    embeddings = []
    metadatas = []
    documents = []

    doc_id = str(uuid.uuid4())

    for i, chunk in enumerate(chunks):
        ids.append(f"{doc_id}_{i}")
        embeddings.append(get_embedding(chunk))
        documents.append(chunk)
        metadatas.append({
            "doc_id": doc_id,
            "chunk_id": f"{doc_id}_{i}",
            "role": "HR"
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    return {"message": "File processed", "doc_id": doc_id}
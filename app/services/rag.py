from app.services.embeddings import get_embedding
from app.db.chroma import collection
from app.services.llm import generate_answer
from app.services.memory import get_history

def rag_pipeline(query, history=None, user_role=None):
    retrieved = retrieve(query, user_role)

    docs = retrieved["documents"]
    metadatas = retrieved["metadatas"]

    prompt = build_prompt(query, docs, history or [])
    answer = generate_answer(prompt)

    if not is_grounded(answer, docs):
        answer = "I don't know based on the provided documents."

    return {
        "answer": answer,
        "sources": metadatas[:1],
        "documents": docs
    }

def retrieve(query, user_role=None, k=3):
    query_embedding = get_embedding(query)

    if user_role:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where={"role": user_role}
        )
    else:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

    return {
        "documents": results["documents"][0],
        "metadatas": results["metadatas"][0]
    }

def build_prompt(query, docs, history):
    context = "\n\n".join(docs)

    history_text = "\n".join([
        f"{m['role']}: {m['content']}" for m in history
    ])

    return f"""
    You must cite sources using provided metadata. Do not invent chunk IDs.
    Conversation History:
    {history_text}

    Context:
    {context}

    Question:
    {query}
    """

def is_grounded(answer, docs):
    for doc in docs:
        for word in answer.lower().split():
            if word in doc.lower():
                return True
    return False
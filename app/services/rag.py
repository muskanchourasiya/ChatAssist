from app.services.embeddings import get_embedding
from app.db.chroma import collection
from app.services.llm import generate_answer

def retrieve(query, k=3):
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]


def build_prompt(query, docs):
    context = "\n\n".join(docs)

    return f"""
You must answer ONLY using the context below.
If answer is not present, say "I don't know".

Context:
{context}

Question:
{query}
"""


def rag_pipeline(query):
    docs = retrieve(query)
    prompt = build_prompt(query, docs)
    return generate_answer(prompt)
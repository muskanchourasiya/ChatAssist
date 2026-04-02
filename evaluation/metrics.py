def retrieval_hit(retrieved_sources, expected_doc_id):
    for src in retrieved_sources:
        if src["doc_id"] == expected_doc_id:
            return 1
    return 0


def answer_match(answer, expected_answer):
    return 1 if expected_answer.lower() in answer.lower() else 0


def hallucination(answer, docs):
    for doc in docs:
        if answer.lower() in doc.lower():
            return 0  
    return 1
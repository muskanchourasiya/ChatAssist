import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from app.services.rag import rag_pipeline

def load_dataset():
    with open("evaluation/dataset.json") as f:
        return json.load(f)


def evaluate():
    data = load_dataset()

    total = len(data)
    retrieval_score = 0
    answer_score = 0
    hallucination_score = 0

    for item in data:
        question = item["question"]
        expected = item["expected_answer"]
        expected_doc = item["doc_id"]

        result = rag_pipeline(question)

        answer = result["answer"]
        sources = result["sources"]

        retrieval_score += any(s["doc_id"] == expected_doc for s in sources)
        answer_score += expected.lower() in answer.lower()

        docs = result.get("documents", []) 
        hallucination_score += 0 if any(answer.lower() in d.lower() for d in docs) else 1

        print(f"\nQ: {question}")
        print(f"A: {answer}")
        print(f"Expected: {expected}")

    print("\n===== FINAL SCORES =====")
    print(f"Retrieval Accuracy: {retrieval_score/total:.2f}")
    print(f"Answer Accuracy: {answer_score/total:.2f}")
    print(f"Hallucination Rate: {hallucination_score/total:.2f}")


if __name__ == "__main__":
    evaluate()
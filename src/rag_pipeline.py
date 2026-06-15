from __future__ import annotations

from src.llm import BaseLLMProvider


class RAGPipeline:
    def __init__(self, llm_provider: BaseLLMProvider) -> None:
        self.llm_provider = llm_provider

    def answer(self, question: str, retrieved_chunks: list[dict], retrieval_plan: str) -> dict:
        context = "\n\n".join(
            [
                f"Source: {chunk['source']} | Metadata: {chunk['metadata']}\n{chunk['text']}"
                for chunk in retrieved_chunks
            ]
        )
        prompt = (
            "Use only the context below to answer the question.\n"
            "If the documents do not contain the answer, reply exactly that the answer was not found in the documents.\n\n"
            f"Retrieval plan:\n{retrieval_plan}\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}"
        )
        llm_response = self.llm_provider.generate(question, prompt, retrieved_chunks)
        return {
            "answer": llm_response.text,
            "sources": retrieved_chunks,
            "mode": llm_response.mode,
            "prompt": prompt,
        }


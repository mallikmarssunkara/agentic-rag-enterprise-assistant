from __future__ import annotations

from src.guardrails import validate_context, validate_grounded_answer, validate_query
from src.rag_pipeline import RAGPipeline
from src.vector_store import FaissVectorStore


class PlannerAgent:
    def plan(self, question: str) -> str:
        return (
            "1. Identify the main business topic in the question.\n"
            "2. Retrieve the most relevant chunks from uploaded files.\n"
            "3. Answer strictly from retrieved evidence.\n"
            f"4. Refuse unsupported claims if the evidence is insufficient.\nQuestion focus: {question}"
        )


class RetrieverAgent:
    def __init__(self, vector_store: FaissVectorStore, embedding_service, top_k: int) -> None:
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.top_k = top_k

    def retrieve(self, question: str) -> list[dict]:
        query_embedding = self.embedding_service.embed_query(question)
        return self.vector_store.search(query_embedding, self.top_k)


class AnswerGeneratorAgent:
    def __init__(self, rag_pipeline: RAGPipeline) -> None:
        self.rag_pipeline = rag_pipeline

    def generate(self, question: str, retrieved_chunks: list[dict], retrieval_plan: str) -> dict:
        return self.rag_pipeline.answer(question, retrieved_chunks, retrieval_plan)


class ValidatorAgent:
    def validate(self, question: str, response: dict) -> dict:
        warnings: list[str] = []

        query_warning = validate_query(question)
        if query_warning:
            warnings.append(query_warning)

        context_warning = validate_context(response.get("sources", []))
        if context_warning:
            warnings.append(context_warning)

        answer_warning = validate_grounded_answer(
            response.get("answer", ""), response.get("sources", [])
        )
        if answer_warning:
            warnings.append(answer_warning)

        return {"is_valid": not warnings, "warnings": warnings}


class AgenticAssistant:
    def __init__(
        self,
        planner: PlannerAgent,
        retriever: RetrieverAgent,
        answer_generator: AnswerGeneratorAgent,
        validator: ValidatorAgent,
    ) -> None:
        self.planner = planner
        self.retriever = retriever
        self.answer_generator = answer_generator
        self.validator = validator

    def ask(self, question: str) -> dict:
        query_warning = validate_query(question)
        if query_warning:
            return {
                "answer": query_warning,
                "sources": [],
                "mode": "guardrail",
                "validation": {"is_valid": False, "warnings": [query_warning]},
            }

        retrieval_plan = self.planner.plan(question)
        sources = self.retriever.retrieve(question)
        context_warning = validate_context(sources)
        if context_warning:
            response = {
                "answer": "The answer was not found in the uploaded documents.",
                "sources": sources,
                "mode": "guardrail",
            }
            response["validation"] = {"is_valid": False, "warnings": [context_warning]}
            return response

        response = self.answer_generator.generate(question, sources, retrieval_plan)
        response["validation"] = self.validator.validate(question, response)
        response["plan"] = retrieval_plan
        return response


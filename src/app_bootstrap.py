from __future__ import annotations

from src.agents import (
    AgenticAssistant,
    AnswerGeneratorAgent,
    PlannerAgent,
    RetrieverAgent,
    ValidatorAgent,
)
from src.config import Settings
from src.embeddings import EmbeddingService
from src.llm import create_llm_provider
from src.rag_pipeline import RAGPipeline
from src.vector_store import FaissVectorStore


def build_assistant(settings: Settings) -> tuple[AgenticAssistant, EmbeddingService, FaissVectorStore]:
    embedding_service = EmbeddingService(settings.embedding_model)
    vector_store = FaissVectorStore(settings.vector_store_dir)
    llm_provider = create_llm_provider(settings.openai_api_key, settings.openai_model)
    rag_pipeline = RAGPipeline(llm_provider)

    assistant = AgenticAssistant(
        planner=PlannerAgent(),
        retriever=RetrieverAgent(vector_store, embedding_service, settings.top_k),
        answer_generator=AnswerGeneratorAgent(rag_pipeline),
        validator=ValidatorAgent(),
    )
    return assistant, embedding_service, vector_store


from __future__ import annotations

import re
from pathlib import Path


def validate_query(query: str) -> str | None:
    if not query or not query.strip():
        return "Please enter a question before requesting an answer."
    return None


def validate_file_type(file_name: str, supported_extensions: tuple[str, ...]) -> str | None:
    if Path(file_name).suffix.lower() not in supported_extensions:
        return f"Unsupported file type for {file_name}."
    return None


def validate_context(results: list[dict], minimum_score: float = 0.20) -> str | None:
    if not results:
        return "The answer was not found in the uploaded documents."
    if max(result.get("score", 0.0) for result in results) < minimum_score:
        return "The retrieved context was too weak to answer confidently from the documents."
    return None


def validate_grounded_answer(answer: str, results: list[dict], minimum_overlap: int = 2) -> str | None:
    if not answer.strip():
        return "The answer generation step did not return content."

    answer_tokens = set(re.findall(r"\b[a-zA-Z]{4,}\b", answer.lower()))
    context_tokens = set()
    for result in results:
        context_tokens.update(re.findall(r"\b[a-zA-Z]{4,}\b", result.get("text", "").lower()))

    overlap = answer_tokens.intersection(context_tokens)
    if len(overlap) < minimum_overlap:
        return "The answer may not be grounded strongly enough in the retrieved evidence."
    return None


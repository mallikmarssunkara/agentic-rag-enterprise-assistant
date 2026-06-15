from src.guardrails import (
    validate_context,
    validate_file_type,
    validate_grounded_answer,
    validate_query,
)


def test_validate_query_rejects_empty() -> None:
    assert validate_query("   ") is not None


def test_validate_file_type_rejects_unknown_extension() -> None:
    assert validate_file_type("notes.docx", (".txt", ".pdf")) is not None


def test_validate_context_rejects_empty_results() -> None:
    assert validate_context([]) is not None


def test_validate_grounded_answer_accepts_overlap() -> None:
    results = [{"text": "Revenue increased due to stronger regional sales execution."}]
    answer = "Regional sales execution increased revenue."
    assert validate_grounded_answer(answer, results) is None


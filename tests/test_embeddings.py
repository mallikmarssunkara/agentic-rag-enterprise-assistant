from src.embeddings import EmbeddingService


def test_hashing_fallback_returns_consistent_vectors() -> None:
    service = EmbeddingService("this-model-does-not-exist")

    first = service.embed_query("finance policy update")
    second = service.embed_query("finance policy update")

    assert service.backend == "hashing"
    assert len(first) == 384
    assert first == second


def test_real_model_loading() -> None:
    service = EmbeddingService("sentence-transformers/all-MiniLM-L6-v2")
    assert service.backend == "sentence-transformer"
    vector = service.embed_query("hello")
    assert len(vector) == 384

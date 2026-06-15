from src.embeddings import EmbeddingService


def test_hashing_fallback_returns_consistent_vectors() -> None:
    service = EmbeddingService("this-model-does-not-exist")

    first = service.embed_query("finance policy update")
    second = service.embed_query("finance policy update")

    assert service.backend == "hashing"
    assert len(first) == 384
    assert first == second

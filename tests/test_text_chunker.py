from src.document_loader import TextDocument
from src.text_chunker import TextChunker


def test_chunk_documents_preserves_metadata() -> None:
    document = TextDocument(
        text="A" * 1200,
        source="policy.txt",
        metadata={"file_type": "txt"},
    )
    chunker = TextChunker(chunk_size=500, chunk_overlap=100)

    chunks = chunker.chunk_documents([document])

    assert len(chunks) >= 2
    assert chunks[0]["source"] == "policy.txt"
    assert chunks[0]["metadata"]["file_type"] == "txt"


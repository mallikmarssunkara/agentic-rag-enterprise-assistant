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


def test_chunk_documents_splits_at_word_boundary() -> None:
    # 'first second third'
    # Length: 18. With chunk_size=10, chunk_overlap=5:
    # A naive split at 10 would yield 'first seco', cutting 'second' in half.
    # The boundary-aware splitter should back up to the space and yield 'first'.
    document = TextDocument(
        text="first second third",
        source="doc.txt",
        metadata={"file_type": "txt"},
    )
    chunker = TextChunker(chunk_size=10, chunk_overlap=5)
    chunks = chunker.chunk_documents([document])

    assert chunks[0]["text"] == "first"
    # Second chunk will pick up from index 1 (or 6 after progress constraint if overlap is small),
    # ensuring no word is cut in half.
    assert "seco" not in chunks[0]["text"]



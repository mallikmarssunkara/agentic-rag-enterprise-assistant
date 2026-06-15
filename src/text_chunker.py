from __future__ import annotations

from src.document_loader import TextDocument


class TextChunker:
    def __init__(self, chunk_size: int, chunk_overlap: int) -> None:
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(self, documents: list[TextDocument]) -> list[dict]:
        chunks: list[dict] = []

        for document in documents:
            text = document.text
            start = 0
            chunk_index = 0

            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                chunk_text = text[start:end].strip()
                if chunk_text:
                    chunks.append(
                        {
                            "text": chunk_text,
                            "source": document.source,
                            "metadata": {**document.metadata, "chunk_index": chunk_index},
                        }
                    )
                    chunk_index += 1

                if end == len(text):
                    break
                start = max(end - self.chunk_overlap, 0)

        return chunks


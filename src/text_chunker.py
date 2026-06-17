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
                if start + self.chunk_size >= len(text):
                    end = len(text)
                else:
                    max_end = start + self.chunk_size
                    # Search window is the overlap region at the end of the chunk
                    search_start = max(max_end - self.chunk_overlap, start + 1)
                    window = text[search_start:max_end]
                    
                    end = max_end  # fallback
                    
                    # 1. Look for paragraph separator
                    para_idx = window.rfind("\n\n")
                    if para_idx != -1:
                        end = search_start + para_idx + 2
                    else:
                        # 2. Look for sentence separator (. or ? or ! followed by space)
                        best_sent_idx = -1
                        for i in range(len(window) - 2, -1, -1):
                            if window[i] in {".", "?", "!"} and window[i+1] == " ":
                                best_sent_idx = i + 1  # split right after punctuation
                                break
                        if best_sent_idx != -1:
                            end = search_start + best_sent_idx
                        else:
                            # 3. Look for single newline
                            nl_idx = window.rfind("\n")
                            if nl_idx != -1:
                                end = search_start + nl_idx + 1
                            else:
                                # 4. Look for space (word boundary)
                                space_idx = window.rfind(" ")
                                if space_idx != -1:
                                    end = search_start + space_idx + 1

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

                if end >= len(text):
                    break

                next_start = max(end - self.chunk_overlap, 0)
                # Ensure forward progress is always made
                if next_start <= start:
                    next_start = start + (self.chunk_size - self.chunk_overlap)
                    if next_start <= start:
                        next_start = start + 1
                start = next_start

        return chunks


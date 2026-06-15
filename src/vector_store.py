from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy as np

from src.utils import ensure_directory


class FaissVectorStore:
    def __init__(self, store_dir: Path) -> None:
        self.store_dir = ensure_directory(store_dir)
        self.index_path = self.store_dir / "index.faiss"
        self.metadata_path = self.store_dir / "metadata.json"
        self.index: faiss.IndexFlatIP | None = None
        self.metadata: list[dict] = []

    def build(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        if not chunks or not embeddings:
            raise ValueError("Chunks and embeddings are required to build the vector store.")

        matrix = np.array(embeddings, dtype="float32")
        dimension = matrix.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(matrix)
        self.metadata = chunks
        self.save()

    def save(self) -> None:
        if self.index is None:
            raise ValueError("Vector index has not been built.")
        faiss.write_index(self.index, str(self.index_path))
        self.metadata_path.write_text(json.dumps(self.metadata, indent=2), encoding="utf-8")

    def load(self) -> bool:
        if not self.index_path.exists() or not self.metadata_path.exists():
            return False
        self.index = faiss.read_index(str(self.index_path))
        self.metadata = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        return True

    def search(self, query_embedding: list[float], top_k: int) -> list[dict]:
        if self.index is None or not self.metadata:
            if not self.load():
                raise ValueError("Vector store is not available. Please ingest documents first.")

        query = np.array([query_embedding], dtype="float32")
        scores, indices = self.index.search(query, top_k)

        results: list[dict] = []
        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue
            result = dict(self.metadata[index])
            result["score"] = float(score)
            results.append(result)
        return results


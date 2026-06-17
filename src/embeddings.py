from __future__ import annotations

import hashlib

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str, fallback_dimension: int = 384) -> None:
        self.model_name = model_name
        self.fallback_dimension = fallback_dimension
        self.backend = "hashing"
        self.model: SentenceTransformer | None = None

        try:
            # Prefer the cached local model so the project remains usable without network access.
            self.model = SentenceTransformer(model_name, local_files_only=True)
            self.backend = "sentence-transformer"
        except Exception:
            try:
                # If the local cache is empty, attempt to download it if online.
                self.model = SentenceTransformer(model_name, local_files_only=False)
                self.backend = "sentence-transformer"
            except Exception:
                self.model = None
                self.backend = "hashing"

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if self.model is not None:
            vectors = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
            return vectors.tolist()
        return [self._hash_embed(text).tolist() for text in texts]

    def embed_query(self, text: str) -> list[float]:
        if self.model is not None:
            vector = self.model.encode([text], convert_to_numpy=True, normalize_embeddings=True)[0]
            return vector.tolist()
        return self._hash_embed(text).tolist()

    def _hash_embed(self, text: str) -> np.ndarray:
        vector = np.zeros(self.fallback_dimension, dtype="float32")
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            bucket = int.from_bytes(digest[:4], "big") % self.fallback_dimension
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[bucket] += sign

        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm

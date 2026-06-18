from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

try:
    import streamlit as st
except Exception:  # pragma: no cover - Streamlit may be unavailable in some test contexts.
    st = None


def get_setting(name: str, default: str) -> str:
    if st is not None:
        try:
            if name in st.session_state and st.session_state[name] not in (None, ""):
                return str(st.session_state[name])
        except Exception:
            pass

    env_value = os.getenv(name)
    if env_value not in (None, ""):
        return env_value

    if st is not None:
        try:
            secret_value = st.secrets.get(name)
            if secret_value not in (None, ""):
                return str(secret_value)
        except Exception:
            pass

    return default


@dataclass(frozen=True)
class Settings:
    upload_dir: Path = BASE_DIR / "data" / "uploaded_docs"
    vector_store_dir: Path = BASE_DIR / "data" / "vector_store"
    chunk_size: int = int(get_setting("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(get_setting("CHUNK_OVERLAP", "150"))
    top_k: int = int(get_setting("TOP_K", "4"))
    embedding_model: str = get_setting(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    openai_api_key: str = get_setting("OPENAI_API_KEY", "")
    openai_model: str = get_setting("OPENAI_MODEL", "gpt-4o-mini")
    supported_extensions: tuple[str, ...] = (".pdf", ".txt", ".csv", ".xlsx", ".xls")


def get_settings() -> Settings:
    load_dotenv(BASE_DIR / ".env", override=True)
    return Settings()

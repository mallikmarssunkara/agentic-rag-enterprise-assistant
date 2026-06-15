from __future__ import annotations

import logging
import re
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def sanitize_filename(filename: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", filename).strip("._")
    return cleaned or "uploaded_file"


def clean_text(text: str) -> str:
    normalized = text.replace("\x00", " ")
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def save_uploaded_file(uploaded_file, destination_dir: Path) -> Path:
    ensure_directory(destination_dir)
    safe_name = sanitize_filename(uploaded_file.name)
    destination = destination_dir / safe_name
    destination.write_bytes(uploaded_file.getbuffer())
    return destination


def format_score(score: float) -> str:
    return f"{score:.4f}"


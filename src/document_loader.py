from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
from pypdf import PdfReader

from src.utils import clean_text, get_logger

logger = get_logger(__name__)


@dataclass
class TextDocument:
    text: str
    source: str
    metadata: dict[str, Any]


class DocumentLoader:
    def __init__(self, supported_extensions: tuple[str, ...]) -> None:
        self.supported_extensions = supported_extensions

    def load_files(self, file_paths: list[Path]) -> tuple[list[TextDocument], list[str]]:
        documents: list[TextDocument] = []
        errors: list[str] = []

        for file_path in file_paths:
            try:
                documents.extend(self.load_file(file_path))
            except Exception as exc:
                message = f"{file_path.name}: {exc}"
                logger.exception("Failed to load file %s", file_path)
                errors.append(message)

        return documents, errors

    def load_file(self, file_path: Path) -> list[TextDocument]:
        suffix = file_path.suffix.lower()
        if suffix not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {suffix}")

        if suffix == ".pdf":
            return self._load_pdf(file_path)
        if suffix == ".txt":
            return self._load_txt(file_path)
        if suffix == ".csv":
            return self._load_csv(file_path)
        if suffix in {".xlsx", ".xls"}:
            return self._load_excel(file_path)

        raise ValueError(f"No loader configured for {suffix}")

    def _load_pdf(self, file_path: Path) -> list[TextDocument]:
        reader = PdfReader(str(file_path))
        pages: list[TextDocument] = []

        for page_index, page in enumerate(reader.pages):
            page_text = clean_text(page.extract_text() or "")
            if page_text:
                pages.append(
                    TextDocument(
                        text=page_text,
                        source=file_path.name,
                        metadata={"page": page_index + 1, "file_type": "pdf"},
                    )
                )

        if not pages:
            raise ValueError("The PDF did not contain extractable text.")
        return pages

    def _load_txt(self, file_path: Path) -> list[TextDocument]:
        text = clean_text(file_path.read_text(encoding="utf-8", errors="ignore"))
        if not text:
            raise ValueError("The text file is empty.")
        return [TextDocument(text=text, source=file_path.name, metadata={"file_type": "txt"})]

    def _load_csv(self, file_path: Path) -> list[TextDocument]:
        dataframe = pd.read_csv(file_path)
        if dataframe.empty and not list(dataframe.columns):
            raise ValueError("The CSV file is empty.")
        text = clean_text(dataframe.to_csv(index=False))
        if not text:
            raise ValueError("The CSV file did not produce usable text.")
        return [TextDocument(text=text, source=file_path.name, metadata={"file_type": "csv"})]

    def _load_excel(self, file_path: Path) -> list[TextDocument]:
        sheets = pd.read_excel(file_path, sheet_name=None)
        documents: list[TextDocument] = []

        for sheet_name, dataframe in sheets.items():
            if dataframe.empty and not list(dataframe.columns):
                continue
            sheet_text = clean_text(
                f"Sheet: {sheet_name}\n{dataframe.to_csv(index=False)}"
            )
            if sheet_text:
                documents.append(
                    TextDocument(
                        text=sheet_text,
                        source=file_path.name,
                        metadata={"file_type": "excel", "sheet_name": sheet_name},
                    )
                )

        if not documents:
            raise ValueError("The Excel file did not contain usable sheet content.")
        return documents


from pathlib import Path

import pandas as pd

from src.document_loader import DocumentLoader


def test_load_txt_file(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Company policy allows remote work on Fridays.", encoding="utf-8")

    loader = DocumentLoader((".txt",))
    documents = loader.load_file(file_path)

    assert len(documents) == 1
    assert "remote work" in documents[0].text


def test_load_csv_file(tmp_path: Path) -> None:
    file_path = tmp_path / "metrics.csv"
    pd.DataFrame([{"department": "Sales", "revenue": 100}]).to_csv(file_path, index=False)

    loader = DocumentLoader((".csv",))
    documents = loader.load_file(file_path)

    assert len(documents) == 1
    assert "Sales" in documents[0].text


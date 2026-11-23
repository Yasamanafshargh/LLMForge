
import json

import pytest

from llmforge.ingestion import JSONLoader


def test_json_loader(tmp_path):

    file_path = tmp_path / "dataset.json"

    data = [
        {
            "id": "1",
            "text": "یادگیری ماشین چیست؟",
            "category": "ML"
        },
        {
            "id": "2",
            "text": "هوش مصنوعی چیست؟",
            "category": "AI"
        }
    ]

    file_path.write_text(
        json.dumps(data, ensure_ascii=False),
        encoding="utf-8"
    )

    loader = JSONLoader()
    documents = loader.load(str(file_path))

    assert len(documents) == 2
    assert documents[0].id == "1"
    assert documents[0].text == "یادگیری ماشین چیست؟"
    assert documents[1].metadata["category"] == "AI"
    assert documents[0].metadata["format"] == "json"


def test_json_loader_custom_text_field(tmp_path):

    file_path = tmp_path / "dataset.json"

    data = {
        "id": "1",
        "question": "هوش مصنوعی چیست؟"
    }

    file_path.write_text(
        json.dumps(data, ensure_ascii=False),
        encoding="utf-8"
    )

    loader = JSONLoader(text_field="question")
    documents = loader.load(str(file_path))

    assert documents[0].text == "هوش مصنوعی چیست؟"


def test_json_loader_missing_text_field(tmp_path):

    file_path = tmp_path / "dataset.json"

    data = {"id": "1", "category": "AI"}

    file_path.write_text(
        json.dumps(data, ensure_ascii=False),
        encoding="utf-8"
    )

    loader = JSONLoader()

    with pytest.raises(ValueError):
        loader.load(str(file_path))

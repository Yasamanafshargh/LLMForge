
import pytest

from llmforge.ingestion import JSONLLoader


def test_jsonl_loader(tmp_path):

    file_path = tmp_path / "dataset.jsonl"

    content = (
        '{"id": "1", "text": "سلام دنیا", "category": "general"}\n'
        '{"id": "2", "text": "یادگیری ماشین", "category": "ML"}\n'
    )

    file_path.write_text(content, encoding="utf-8")

    loader = JSONLLoader()
    documents = loader.load(str(file_path))

    assert len(documents) == 2
    assert documents[0].text == "سلام دنیا"
    assert documents[1].text == "یادگیری ماشین"
    assert documents[0].metadata["format"] == "jsonl"


def test_jsonl_loader_ignores_empty_lines(tmp_path):

    file_path = tmp_path / "dataset.jsonl"

    content = (
        '{"id": "1", "text": "سلام"}\n'
        '\n'
        '{"id": "2", "text": "خداحافظ"}\n'
    )

    file_path.write_text(content, encoding="utf-8")

    loader = JSONLLoader()
    documents = loader.load(str(file_path))

    assert len(documents) == 2


def test_jsonl_loader_invalid_json(tmp_path):

    file_path = tmp_path / "dataset.jsonl"

    file_path.write_text(
        '{"id": "1", "text": "سلام"}\n'
        '{"id": "2", "text": \n',
        encoding="utf-8"
    )

    loader = JSONLLoader()

    with pytest.raises(ValueError, match="Invalid JSON"):
        loader.load(str(file_path))


import pytest

from llmforge.ingestion import CSVLoader


def test_csv_loader(tmp_path):

    file_path = tmp_path / "dataset.csv"

    content = (
        "id,question,answer,category\n"
        "1,هوش مصنوعی چیست؟,هوش مصنوعی شاخه‌ای از علوم کامپیوتر است.,AI\n"
        "2,یادگیری ماشین چیست؟,یادگیری ماشین از داده یاد می‌گیرد.,ML\n"
    )

    file_path.write_text(content, encoding="utf-8")

    loader = CSVLoader(text_field="answer")
    documents = loader.load(str(file_path))

    assert len(documents) == 2
    assert documents[0].text == "هوش مصنوعی شاخه‌ای از علوم کامپیوتر است."
    assert documents[0].metadata["question"] == "هوش مصنوعی چیست؟"
    assert documents[1].metadata["category"] == "ML"
    assert documents[0].metadata["format"] == "csv"


def test_csv_loader_missing_column(tmp_path):

    file_path = tmp_path / "dataset.csv"

    content = (
        "id,question,category\n"
        "1,هوش مصنوعی چیست؟,AI\n"
    )

    file_path.write_text(content, encoding="utf-8")

    loader = CSVLoader(text_field="answer")

    with pytest.raises(ValueError, match="not found"):
        loader.load(str(file_path))

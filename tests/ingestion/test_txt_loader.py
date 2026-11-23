
from llmforge.ingestion import TXTLoader


def test_txt_loader(tmp_path):

    # Arrange: create a temporary Persian text file
    file_path = tmp_path / "sample.txt"

    expected_text = "یادگیری ماشین یکی از شاخه‌های هوش مصنوعی است."

    file_path.write_text(
        expected_text,
        encoding="utf-8"
    )

    # Act: load the file
    loader = TXTLoader()
    documents = loader.load(str(file_path))

    # Assert: verify the result
    assert len(documents) == 1
    assert documents[0].text == expected_text
    assert documents[0].id == "sample"
    assert documents[0].metadata["format"] == "txt"

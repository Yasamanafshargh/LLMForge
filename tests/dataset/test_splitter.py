
import pytest

from llmforge.core.document import Document
from llmforge.dataset import DatasetSplitter


@pytest.fixture
def documents():
    return [
        Document(id=f"doc_{i}", text=f"Document number {i}")
        for i in range(10)
    ]


def test_default_split_ratios(documents):
    splitter = DatasetSplitter()
    result = splitter.split(documents)

    assert len(result["train"]) == 8
    assert len(result["validation"]) == 1
    assert len(result["test"]) == 1


def test_reproducible_split(documents):
    splitter = DatasetSplitter(seed=42)

    first = splitter.split(documents)
    second = splitter.split(documents)

    assert [d.id for d in first["train"]] == [
        d.id for d in second["train"]
    ]


def test_different_seeds(documents):
    first = DatasetSplitter(seed=42).split(documents)
    second = DatasetSplitter(seed=100).split(documents)

    assert [d.id for d in first["train"]] != [
        d.id for d in second["train"]
    ]


def test_no_document_is_lost_or_duplicated(documents):
    result = DatasetSplitter().split(documents)

    all_ids = [
        doc.id
        for subset in result.values()
        for doc in subset
    ]

    assert len(all_ids) == len(documents)
    assert set(all_ids) == {doc.id for doc in documents}


def test_original_list_is_not_modified(documents):
    original_ids = [doc.id for doc in documents]

    DatasetSplitter().split(documents)

    assert [doc.id for doc in documents] == original_ids


def test_small_dataset_can_have_empty_subset():
    small_documents = [
        Document(id=f"doc_{i}", text=f"Text {i}")
        for i in range(5)
    ]

    result = DatasetSplitter().split(small_documents)

    assert len(result["train"]) == 4
    assert len(result["validation"]) == 0
    assert len(result["test"]) == 1


def test_invalid_ratios():
    with pytest.raises(ValueError):
        DatasetSplitter(
            train_ratio=0.8,
            validation_ratio=0.3,
            test_ratio=0.1,
        )


def test_duplicate_document_ids():
    documents = [
        Document(id="same_id", text="First"),
        Document(id="same_id", text="Second"),
    ]

    with pytest.raises(ValueError):
        DatasetSplitter().split(documents)

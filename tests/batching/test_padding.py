
import pytest

from llmforge.core.document import Document
from llmforge.batching import PaddingStage


@pytest.fixture
def documents():
    return [
        Document(id="1", text="A", token_ids=[4, 5, 6]),
        Document(id="2", text="B", token_ids=[8, 9]),
        Document(id="3", text="C", token_ids=[2, 3, 4, 5]),
    ]


def test_dynamic_padding(documents):

    stage = PaddingStage(pad_token_id=0)

    result = stage.process(documents)

    assert [doc.token_ids for doc in result] == [
        [4, 5, 6, 0],
        [8, 9, 0, 0],
        [2, 3, 4, 5],
    ]


def test_attention_masks(documents):

    stage = PaddingStage()

    result = stage.process(documents)

    assert [
        doc.metadata["attention_mask"]
        for doc in result
    ] == [
        [1, 1, 1, 0],
        [1, 1, 0, 0],
        [1, 1, 1, 1],
    ]


def test_fixed_length_padding(documents):

    stage = PaddingStage(
        max_length=5,
        truncation=True
    )

    result = stage.process(documents)

    assert all(len(doc.token_ids) == 5 for doc in result)


def test_truncation(documents):

    stage = PaddingStage(
        max_length=2,
        truncation=True
    )

    result = stage.process(documents)

    assert [doc.token_ids for doc in result] == [
        [4, 5],
        [8, 9],
        [2, 3],
    ]


def test_padding_disabled(documents):

    stage = PaddingStage(padding=False)

    result = stage.process(documents)

    assert [doc.token_ids for doc in result] == [
        [4, 5, 6],
        [8, 9],
        [2, 3, 4, 5],
    ]

    assert [
        doc.metadata["attention_mask"]
        for doc in result
    ] == [
        [1, 1, 1],
        [1, 1],
        [1, 1, 1, 1],
    ]


def test_empty_batch():

    stage = PaddingStage()

    assert stage.process([]) == []


def test_invalid_input():

    stage = PaddingStage()

    with pytest.raises(TypeError):
        stage.process("not a document list")


def test_invalid_pad_token():

    with pytest.raises(ValueError):
        PaddingStage(pad_token_id=-1)


def test_invalid_max_length():

    with pytest.raises(ValueError):
        PaddingStage(max_length=0)


def test_invalid_fixed_length_configuration():

    with pytest.raises(ValueError):
        PaddingStage(max_length=3)


def test_invalid_document_item():

    stage = PaddingStage()

    with pytest.raises(TypeError):
        stage.process(["not a document"])


def test_invalid_token_id():

    document = Document(
        id="1",
        text="test",
        token_ids=[4, -1]
    )

    stage = PaddingStage()

    with pytest.raises(ValueError):
        stage.process([document])

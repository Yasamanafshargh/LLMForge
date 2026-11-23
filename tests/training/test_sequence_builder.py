
import pytest

from llmforge.core.document import Document
from llmforge.training import SequenceBuilder, TrainingExample


@pytest.fixture
def documents():
    return [
        Document(
            id="doc_1",
            text="First document",
            token_ids=[2, 15, 28, 9, 3],
        ),
        Document(
            id="doc_2",
            text="Second document",
            token_ids=[2, 40, 12, 3],
        ),
    ]


def test_build_input_and_target_sequences(documents):
    builder = SequenceBuilder()
    examples = builder.build(documents)

    assert examples[0].input_ids == [2, 15, 28, 9]
    assert examples[0].target_ids == [15, 28, 9, 3]


def test_returns_training_examples(documents):
    examples = SequenceBuilder().build(documents)

    assert all(
        isinstance(example, TrainingExample)
        for example in examples
    )


def test_preserves_document_ids(documents):
    examples = SequenceBuilder().build(documents)

    assert examples[0].document_id == "doc_1"
    assert examples[1].document_id == "doc_2"


def test_input_and_target_lengths_are_equal(documents):
    examples = SequenceBuilder().build(documents)

    for example in examples:
        assert len(example.input_ids) == len(example.target_ids)


def test_documents_are_processed_independently(documents):
    examples = SequenceBuilder().build(documents)

    assert examples[0].target_ids[-1] == 3
    assert examples[1].input_ids[0] == 2


def test_empty_document_list():
    assert SequenceBuilder().build([]) == []


def test_document_with_insufficient_tokens():
    document = Document(
        id="doc_1",
        text="",
        token_ids=[2],
    )

    with pytest.raises(ValueError):
        SequenceBuilder().build([document])


def test_invalid_token_ids():
    document = Document(
        id="doc_1",
        text="Test",
        token_ids=[2, -5, 3],
    )

    with pytest.raises(ValueError):
        SequenceBuilder().build([document])


def test_invalid_input_type():
    with pytest.raises(TypeError):
        SequenceBuilder().build("not a document list")



import pytest

from llmforge.training import (
    TrainingExample,
    CausalLMCollator,
    TrainingBatch,
)


@pytest.fixture
def examples():
    return [
        TrainingExample(
            document_id="doc_1",
            input_ids=[2, 15, 28, 9],
            target_ids=[15, 28, 9, 3],
        ),
        TrainingExample(
            document_id="doc_2",
            input_ids=[2, 40, 12],
            target_ids=[40, 12, 3],
        ),
    ]


def test_returns_training_batch(examples):
    batch = CausalLMCollator()(examples)

    assert isinstance(batch, TrainingBatch)


def test_pads_input_sequences(examples):
    batch = CausalLMCollator()(examples)

    assert batch.input_ids == [
        [2, 15, 28, 9],
        [2, 40, 12, 0],
    ]


def test_pads_targets_with_ignore_index(examples):
    batch = CausalLMCollator()(examples)

    assert batch.target_ids == [
        [15, 28, 9, 3],
        [40, 12, 3, -100],
    ]


def test_generates_attention_masks(examples):
    batch = CausalLMCollator()(examples)

    assert batch.attention_mask == [
        [1, 1, 1, 1],
        [1, 1, 1, 0],
    ]


def test_preserves_document_ids(examples):
    batch = CausalLMCollator()(examples)

    assert batch.document_ids == ["doc_1", "doc_2"]


def test_custom_padding_values():
    example = [
        TrainingExample(
            document_id="doc_1",
            input_ids=[2, 15],
            target_ids=[15, 3],
        ),
        TrainingExample(
            document_id="doc_2",
            input_ids=[2],
            target_ids=[3],
        ),
    ]

    batch = CausalLMCollator(
        pad_token_id=99,
        ignore_index=-1,
    )(example)

    assert batch.input_ids[1] == [2, 99]
    assert batch.target_ids[1] == [3, -1]


def test_empty_examples():
    batch = CausalLMCollator()([])

    assert batch.input_ids == []
    assert batch.target_ids == []
    assert batch.attention_mask == []


def test_input_target_length_mismatch():
    example = [
        TrainingExample(
            document_id="doc_1",
            input_ids=[2, 15],
            target_ids=[15],
        )
    ]

    with pytest.raises(ValueError):
        CausalLMCollator()(example)


def test_invalid_token_ids():
    example = [
        TrainingExample(
            document_id="doc_1",
            input_ids=[2, -5],
            target_ids=[-5, 3],
        )
    ]

    with pytest.raises(ValueError):
        CausalLMCollator()(example)


def test_original_examples_are_not_modified(examples):
    original_inputs = [
        example.input_ids.copy()
        for example in examples
    ]

    original_targets = [
        example.target_ids.copy()
        for example in examples
    ]

    CausalLMCollator()(examples)

    assert [
        example.input_ids for example in examples
    ] == original_inputs

    assert [
        example.target_ids for example in examples
    ] == original_targets


def test_invalid_input_type():
    with pytest.raises(TypeError):
        CausalLMCollator()("not a list")


import pytest

from llmforge.tokenization.bpe.bpe_trainer import BPETrainer


@pytest.fixture
def trained_trainer():
    trainer = BPETrainer()

    trainer.train(
        ["banana", "banana", "bandana"],
        num_merges=3
    )

    return trainer


def test_initial_vocabulary(trained_trainer):
    assert trained_trainer.initial_vocabulary == [
        "b", "a", "n", "d"
    ]


def test_complete_vocabulary(trained_trainer):
    model = trained_trainer.build_model()

    expected_tokens = [
        "[PAD]",
        "[UNK]",
        "[BOS]",
        "[EOS]",
        "b",
        "a",
        "n",
        "d",
        "an",
        "ban",
        "ana"
    ]

    assert model.vocabulary == expected_tokens


def test_intermediate_tokens_are_in_vocabulary(trained_trainer):
    model = trained_trainer.build_model()

    assert "an" in model.vocabulary
    assert "ban" in model.vocabulary
    assert "ana" in model.vocabulary


def test_vocabulary_has_no_duplicates(trained_trainer):
    model = trained_trainer.build_model()

    assert len(model.vocabulary) == len(set(model.vocabulary))


def test_empty_training_corpus():
    trainer = BPETrainer()

    trainer.train([], num_merges=3)

    with pytest.raises(RuntimeError):
        trainer.build_model()

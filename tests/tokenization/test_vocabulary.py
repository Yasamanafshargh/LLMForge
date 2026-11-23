
import pytest

from llmforge.tokenization.vocabulary import Vocabulary


@pytest.fixture
def vocabulary():
    vocab = Vocabulary()
    vocab.build(["I", "love", "AI", "I", "love"])
    return vocab


def test_vocabulary_building(vocabulary):
    assert len(vocabulary) == 7

    assert vocabulary.token_to_id["[PAD]"] == 0
    assert vocabulary.token_to_id["[UNK]"] == 1
    assert vocabulary.token_to_id["I"] == 4


def test_duplicate_tokens(vocabulary):
    assert len(vocabulary) == 7
    assert vocabulary.token_to_id["I"] == 4
    assert vocabulary.token_to_id["love"] == 5


def test_unknown_token(vocabulary):
    result = vocabulary.encode(["I", "robotics"])

    assert result == [4, 1]


def test_add_bos_token(vocabulary):
    result = vocabulary.encode(
        ["I", "love"],
        add_bos=True
    )

    assert result == [2, 4, 5]


def test_add_eos_token(vocabulary):
    result = vocabulary.encode(
        ["I", "love"],
        add_eos=True
    )

    assert result == [4, 5, 3]


def test_round_trip(vocabulary):
    tokens = ["I", "love", "AI"]

    encoded = vocabulary.encode(tokens)
    decoded = vocabulary.decode(encoded)

    assert decoded == tokens


def test_duplicate_special_tokens():
    with pytest.raises(ValueError):
        Vocabulary(special_tokens=["[UNK]", "[UNK]"])


def test_encode_before_build():
    vocab = Vocabulary()

    with pytest.raises(RuntimeError):
        vocab.encode(["hello"])


def test_invalid_token_id(vocabulary):
    with pytest.raises(ValueError):
        vocabulary.decode([999])

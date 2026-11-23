
import pytest

from llmforge.tokenization.bpe.bpe_tokenizer import BPETokenizer
from llmforge.tokenization.bpe.bpe_model import BPEModel

@pytest.fixture
def tokenizer():
    merges = [
        ("a", "n"),
        ("b", "an"),
        ("an", "a")
    ]

    return BPETokenizer(merges)


def test_basic_bpe_tokenization(tokenizer):
    result = tokenizer.tokenize("banana")

    assert result == ["ban", "ana"]


def test_word_boundaries_are_preserved(tokenizer):
    result = tokenizer.tokenize("banana bandana")

    assert result == ["ban", "ana", "ban", "d", "ana"]


def test_punctuation_is_separate(tokenizer):
    result = tokenizer.tokenize("banana!")

    assert result == ["ban", "ana", "!"]


def test_spacing_reconstruction(tokenizer):
    text = "  banana   bandana!  "

    result = tokenizer.tokenize_with_spacing(text)

    assert result.reconstruct() == text


def test_punctuation_spacing(tokenizer):
    text = "banana, bandana !"

    result = tokenizer.tokenize_with_spacing(text)

    assert result.reconstruct() == text


def test_empty_text(tokenizer):
    result = tokenizer.tokenize("")

    assert result == []


def test_empty_text_with_spacing(tokenizer):
    result = tokenizer.tokenize_with_spacing("")

    assert result.tokens == []
    assert result.separators == [""]
    assert result.reconstruct() == ""


def test_invalid_input(tokenizer):
    with pytest.raises(TypeError):
        tokenizer.tokenize(123)


def test_invalid_input_with_spacing(tokenizer):
    with pytest.raises(TypeError):
        tokenizer.tokenize_with_spacing(123)


def test_create_tokenizer_from_model():
    model = BPEModel(
        merges=[
            ("a", "n"),
            ("b", "an"),
            ("an", "a")
        ]
    )

    tokenizer = BPETokenizer.from_model(model)

    assert tokenizer.merges == model.merges

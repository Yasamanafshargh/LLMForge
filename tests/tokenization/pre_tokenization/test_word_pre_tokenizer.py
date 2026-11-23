
import pytest

from llmforge.tokenization.pre_tokenization import WordPreTokenizer


@pytest.fixture
def tokenizer():
    return WordPreTokenizer()


def test_english_text(tokenizer):
    result = tokenizer.tokenize("I love Python!")
    assert result == ["I", "love", "Python", "!"]


def test_persian_text(tokenizer):
    result = tokenizer.tokenize("من به هوش مصنوعی علاقه‌مند هستم.")
    assert result == [
        "من", "به", "هوش", "مصنوعی", "علاقه‌مند", "هستم", "."
    ]


def test_preserves_zwnj(tokenizer):
    result = tokenizer.tokenize("کتاب‌ها")
    assert result == ["کتاب‌ها"]


def test_mixed_language(tokenizer):
    result = tokenizer.tokenize("من Python را دوست دارم!")
    assert result == ["من", "Python", "را", "دوست", "دارم", "!"]


def test_decimal_numbers(tokenizer):
    result = tokenizer.tokenize("Python 3.13 is great.")
    assert result == ["Python", "3.13", "is", "great", "."]


def test_empty_text(tokenizer):
    assert tokenizer.tokenize("") == []


def test_invalid_input(tokenizer):
    with pytest.raises(TypeError):
        tokenizer.tokenize(123)


def test_preserves_whitespace(tokenizer):
    text = "  I love   Python programming!  "

    result = tokenizer.pre_tokenize(text)

    assert result.reconstruct() == text


def test_preserves_leading_and_trailing_whitespace(tokenizer):
    text = "   Hello world   "

    result = tokenizer.pre_tokenize(text)

    assert result.separators[0] == "   "
    assert result.separators[-1] == "   "


def test_preserves_punctuation_spacing(tokenizer):
    text = "Hello,   world !"

    result = tokenizer.pre_tokenize(text)

    assert result.reconstruct() == text


def test_empty_text_result(tokenizer):
    result = tokenizer.pre_tokenize("")

    assert result.tokens == []
    assert result.separators == [""]
    assert result.reconstruct() == ""


def test_separator_count(tokenizer):
    result = tokenizer.pre_tokenize("I love Python!")

    assert len(result.separators) == len(result.tokens) + 1

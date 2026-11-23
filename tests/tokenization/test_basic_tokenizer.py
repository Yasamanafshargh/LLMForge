import pytest

from llmforge.tokenization import BasicTokenizer


@pytest.fixture
def tokenizer():
    return BasicTokenizer()


def test_english_tokenization(tokenizer):
    result = tokenizer.tokenize("Hello, world!")

    assert result == ["Hello", ",", "world", "!"]


def test_persian_tokenization(tokenizer):
    result = tokenizer.tokenize("سلام، دنیا!")

    assert result == ["سلام", "،", "دنیا", "!"]


def test_preserve_persian_half_space(tokenizer):
    result = tokenizer.tokenize("کتاب‌هایمان")

    assert result == ["کتاب\u200cهایمان"]


def test_mixed_language(tokenizer):
    result = tokenizer.tokenize("من Python را دوست دارم!")

    assert result == ["من", "Python", "را", "دوست", "دارم", "!"]


def test_decimal_number(tokenizer):
    result = tokenizer.tokenize("نسخه 3.13 منتشر شد.")

    assert result == ["نسخه", "3.13", "منتشر", "شد", "."]


def test_hyphenated_word(tokenizer):
    result = tokenizer.tokenize("GPT-4")

    assert result == ["GPT", "-", "4"]


def test_empty_text(tokenizer):
    assert tokenizer.tokenize("") == []


def test_whitespace_only(tokenizer):
    assert tokenizer.tokenize("   \n\t ") == []


def test_invalid_input(tokenizer):
    with pytest.raises(TypeError):
        tokenizer.tokenize(123)
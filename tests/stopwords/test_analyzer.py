
import pytest

from llmforge.stopwords import StopWordAnalyzer


@pytest.fixture
def analyzer():
    return StopWordAnalyzer()


def test_english_stop_words(analyzer):
    result = analyzer.analyze(
        "The model is learning from data.",
        languages=("english",),
    )

    assert result.total_tokens == 6
    assert result.stop_word_count == 3
    assert result.frequencies == {
        "the": 1,
        "is": 1,
        "from": 1,
    }

def test_persian_stop_words(analyzer):
    result = analyzer.analyze(
        "این مدل در حال یادگیری از داده است.",
        languages=("persian",),
    )

    assert result.total_tokens == 8
    assert result.stop_word_count == 4
    assert result.stop_word_percentage == 50.0

    assert result.frequencies == {
        "این": 1,
        "در": 1,
        "از": 1,
        "است": 1,
    }

def test_empty_text(analyzer):
    result = analyzer.analyze("")

    assert result.total_tokens == 0
    assert result.stop_word_count == 0
    assert result.stop_word_percentage == 0.0


def test_punctuation_is_not_counted(analyzer):
    result = analyzer.analyze(
        "The model, is learning!",
        languages=("english",),
    )

    assert result.total_tokens == 4
    assert result.stop_word_count == 2


def test_invalid_language(analyzer):
    with pytest.raises(ValueError):
        analyzer.analyze(
            "Hello world",
            languages=("unknown",),
        )


def test_invalid_input(analyzer):
    with pytest.raises(TypeError):
        analyzer.analyze(123)


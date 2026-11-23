
import pytest

from llmforge.chunking import SentenceChunker


def test_basic_sentence_chunking():
    text = "Sentence one. Sentence two. Sentence three. Sentence four."

    chunker = SentenceChunker(sentences_per_chunk=2)
    chunks = chunker.chunk(text)

    assert len(chunks) == 2
    assert chunks[0] == "Sentence one. Sentence two."
    assert chunks[1] == "Sentence three. Sentence four."


def test_persian_sentence_chunking():
    text = (
        "یادگیری ماشین مهم است. "
        "هوش مصنوعی کاربردهای زیادی دارد. "
        "شبکه‌های عصبی بسیار کاربردی هستند."
    )

    chunker = SentenceChunker(sentences_per_chunk=2)
    chunks = chunker.chunk(text)

    assert len(chunks) == 2
    assert "یادگیری ماشین" in chunks[0]


def test_half_space_preservation():
    text = "می‌روم. کتاب‌ها جالب هستند."

    chunker = SentenceChunker(sentences_per_chunk=2)
    chunks = chunker.chunk(text)

    assert "\u200c" in chunks[0]


def test_whitespace_normalization():
    text = "Hello    world.    Another   sentence."

    chunker = SentenceChunker(sentences_per_chunk=2)
    chunks = chunker.chunk(text)

    assert chunks[0] == "Hello world. Another sentence."


def test_empty_input():
    chunker = SentenceChunker()

    assert chunker.chunk("") == []
    assert chunker.chunk("   ") == []

def test_invalid_input():
    chunker = SentenceChunker()

    with pytest.raises(TypeError):
        chunker.chunk(123)


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        SentenceChunker(sentences_per_chunk=0)


def test_single_sentence():
    text = "This is one sentence."

    chunker = SentenceChunker(sentences_per_chunk=3)
    chunks = chunker.chunk(text)

    assert len(chunks) == 1
    assert chunks[0] == text

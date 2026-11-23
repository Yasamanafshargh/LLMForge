
import pytest

from llmforge.core.document import Document
from llmforge.encoding import TokenEncodingStage
from llmforge.tokenization.basic_tokenizer import BasicTokenizer
from llmforge.tokenization.vocabulary import Vocabulary


@pytest.fixture
def vocabulary():
    vocab = Vocabulary()

    vocab.build([
        "Hello",
        "world",
        "!",
        "I",
        "love",
        "Python",
    ])

    return vocab


def test_basic_encoding(vocabulary):
    document = Document(
        id="doc_1",
        text="Hello world!"
    )

    stage = TokenEncodingStage(
        tokenizer=BasicTokenizer(),
        vocabulary=vocabulary
    )

    result = stage.process(document)

    assert result.tokens == ["Hello", "world", "!"]
    assert result.token_ids == [4, 5, 6]


def test_encoding_with_bos_and_eos(vocabulary):
    document = Document(
        id="doc_2",
        text="Hello world!"
    )

    stage = TokenEncodingStage(
        tokenizer=BasicTokenizer(),
        vocabulary=vocabulary,
        add_bos=True,
        add_eos=True
    )

    result = stage.process(document)

    assert result.token_ids == [2, 4, 5, 6, 3]


def test_unknown_token(vocabulary):
    document = Document(
        id="doc_3",
        text="Hello universe!"
    )

    stage = TokenEncodingStage(
        tokenizer=BasicTokenizer(),
        vocabulary=vocabulary
    )

    result = stage.process(document)

    assert result.token_ids == [4, 1, 6]


def test_empty_document(vocabulary):
    document = Document(
        id="doc_4",
        text=""
    )

    stage = TokenEncodingStage(
        tokenizer=BasicTokenizer(),
        vocabulary=vocabulary
    )

    result = stage.process(document)

    assert result.tokens == []
    assert result.token_ids == []


def test_invalid_document(vocabulary):
    stage = TokenEncodingStage(
        tokenizer=BasicTokenizer(),
        vocabulary=vocabulary
    )

    with pytest.raises(TypeError):
        stage.process("Hello world!")

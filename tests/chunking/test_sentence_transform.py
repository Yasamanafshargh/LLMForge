
import pytest

from llmforge.core.document import Document
from llmforge.chunking import SentenceChunkTransform


def test_transform_creates_multiple_documents():
    document = Document(
        id="doc_1",
        text="First sentence. Second sentence. Third sentence."
    )

    transform = SentenceChunkTransform(sentences_per_chunk=1)
    chunks = transform.transform(document)

    assert len(chunks) == 3
    assert all(isinstance(chunk, Document) for chunk in chunks)


def test_chunk_ids():
    document = Document(
        id="doc_1",
        text="First sentence. Second sentence."
    )

    transform = SentenceChunkTransform(sentences_per_chunk=1)
    chunks = transform.transform(document)

    assert chunks[0].id == "doc_1_chunk_0"
    assert chunks[1].id == "doc_1_chunk_1"


def test_metadata_preservation():
    document = Document(
        id="doc_1",
        text="First sentence. Second sentence.",
        metadata={"language": "en", "category": "test"}
    )

    transform = SentenceChunkTransform(sentences_per_chunk=1)
    chunks = transform.transform(document)

    assert chunks[0].metadata["language"] == "en"
    assert chunks[0].metadata["category"] == "test"


def test_chunk_metadata():
    document = Document(
        id="doc_1",
        text="First sentence. Second sentence."
    )

    transform = SentenceChunkTransform(sentences_per_chunk=1)
    chunks = transform.transform(document)

    assert chunks[0].metadata["parent_document_id"] == "doc_1"
    assert chunks[0].metadata["chunk_index"] == 0
    assert chunks[1].metadata["chunk_index"] == 1
    assert chunks[0].metadata["total_chunks"] == 2


def test_empty_document():
    document = Document(
        id="empty_doc",
        text=""
    )

    transform = SentenceChunkTransform()
    chunks = transform.transform(document)

    assert chunks == []


def test_original_document_is_not_modified():
    document = Document(
        id="doc_1",
        text="First sentence. Second sentence.",
        metadata={"language": "en"}
    )

    original_text = document.text
    original_metadata = document.metadata.copy()

    transform = SentenceChunkTransform(sentences_per_chunk=1)
    transform.transform(document)

    assert document.text == original_text
    assert document.metadata == original_metadata


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        SentenceChunkTransform(sentences_per_chunk=0)

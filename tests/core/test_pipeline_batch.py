
import pytest

from llmforge.core.document import Document
from llmforge.core.pipeline import Pipeline
from llmforge.core.stage import ProcessingStage
from llmforge.core.transform import DocumentTransform
from llmforge.batching.base_batch_stage import BatchProcessingStage
from llmforge.batching.padding import PaddingStage


class AddPrefixStage(ProcessingStage):

    def process(self, document):
        document.text = "Processed: " + document.text
        return document


class DuplicateTransform(DocumentTransform):

    def transform(self, document):
        return [
            Document(
                id=f"{document.id}_1",
                text=document.text,
                token_ids=document.token_ids.copy()
            ),
            Document(
                id=f"{document.id}_2",
                text=document.text,
                token_ids=document.token_ids.copy()
            )
        ]


class CountingBatchStage(BatchProcessingStage):

    def __init__(self):
        self.received_count = None

    def process(self, documents):
        self.received_count = len(documents)
        return documents


def test_processing_stage():
    document = Document(id="1", text="Hello")

    pipeline = Pipeline([AddPrefixStage()])

    result = pipeline.run(document)

    assert len(result) == 1
    assert result[0].text == "Processed: Hello"


def test_batch_processing_stage():
    documents = [
        Document(id="1", text="A"),
        Document(id="2", text="B"),
    ]

    batch_stage = CountingBatchStage()
    pipeline = Pipeline([batch_stage])

    result = pipeline.run_batch(documents)

    assert len(result) == 2
    assert batch_stage.received_count == 2


def test_document_transform():
    document = Document(id="1", text="Hello")

    pipeline = Pipeline([DuplicateTransform()])

    result = pipeline.run(document)

    assert len(result) == 2
    assert result[0].id == "1_1"
    assert result[1].id == "1_2"


def test_transform_then_batch():
    documents = [
        Document(id="1", text="A"),
        Document(id="2", text="B"),
    ]

    batch_stage = CountingBatchStage()

    pipeline = Pipeline([
        DuplicateTransform(),
        batch_stage
    ])

    result = pipeline.run_batch(documents)

    assert len(result) == 4
    assert batch_stage.received_count == 4


def test_encoding_padding_pipeline():
    documents = [
        Document(id="1", text="A", token_ids=[4, 5, 6]),
        Document(id="2", text="B", token_ids=[8, 9]),
    ]

    pipeline = Pipeline([
        PaddingStage(pad_token_id=0)
    ])

    result = pipeline.run_batch(documents)

    assert result[0].token_ids == [4, 5, 6]
    assert result[1].token_ids == [8, 9, 0]

    assert result[1].metadata["attention_mask"] == [1, 1, 0]


def test_empty_batch():
    pipeline = Pipeline([PaddingStage()])

    assert pipeline.run_batch([]) == []


def test_invalid_single_document():
    pipeline = Pipeline([])

    with pytest.raises(TypeError):
        pipeline.run("not a document")


def test_invalid_batch():
    pipeline = Pipeline([])

    with pytest.raises(TypeError):
        pipeline.run_batch(["not a document"])


def test_unsupported_stage():

    class UnknownStage:
        pass

    pipeline = Pipeline([UnknownStage()])

    with pytest.raises(TypeError):
        pipeline.run(Document(id="1", text="Hello"))

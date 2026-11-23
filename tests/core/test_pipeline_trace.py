
import pytest

from llmforge.core.document import Document
from llmforge.core.pipeline import Pipeline
from llmforge.core.stage import ProcessingStage
from llmforge.core.transform import DocumentTransform
from llmforge.batching.base_batch_stage import BatchProcessingStage
from llmforge.core.trace import PipelineExecutionError


# -------------------------
# Test stages
# -------------------------

class AppendTextStage(ProcessingStage):

    def __init__(self, suffix=" processed"):
        self.suffix = suffix

    def process(self, document):
        document.text += self.suffix
        return document


class SplitTransform(DocumentTransform):

    def transform(self, document):
        first = document.model_copy(deep=True)
        second = document.model_copy(deep=True)

        first.text += " part 1"
        second.text += " part 2"

        return [first, second]


class BatchMarker(BatchProcessingStage):

    def process(self, documents):
        for document in documents:
            document.metadata["batched"] = True

        return documents


class FailingStage(ProcessingStage):

    def process(self, document):
        raise ValueError("Intentional test failure")


# -------------------------
# Tests
# -------------------------

def test_trace_captures_stage_input_and_output():

    document = Document(id="1", text="Hello")

    pipeline = Pipeline([
        AppendTextStage(" World")
    ])

    result, trace = pipeline.run_with_trace(document)

    assert result[0].text == "Hello World"

    stage_trace = trace.stages[0]

    assert stage_trace.input_documents[0].text == "Hello"
    assert stage_trace.output_documents[0].text == "Hello World"


def test_trace_captures_stage_configuration():

    pipeline = Pipeline([
        AppendTextStage("!")
    ])

    _, trace = pipeline.run_with_trace(
        Document(id="1", text="Hello")
    )

    assert trace.stages[0].configuration["suffix"] == "!"


def test_trace_records_execution_duration():

    pipeline = Pipeline([
        AppendTextStage()
    ])

    _, trace = pipeline.run_with_trace(
        Document(id="1", text="Hello")
    )

    assert trace.stages[0].duration_ms >= 0
    assert trace.total_duration_ms >= 0


def test_trace_captures_transform_multiple_outputs():

    pipeline = Pipeline([
        SplitTransform()
    ])

    result, trace = pipeline.run_with_trace(
        Document(id="1", text="Hello")
    )

    assert len(result) == 2

    assert len(trace.stages[0].input_documents) == 1
    assert len(trace.stages[0].output_documents) == 2


def test_trace_captures_batch_stage():

    documents = [
        Document(id="1", text="Hello"),
        Document(id="2", text="World"),
    ]

    pipeline = Pipeline([
        BatchMarker()
    ])

    result, trace = pipeline.run_batch_with_trace(documents)

    assert len(result) == 2
    assert all(
        doc.metadata["batched"] is True
        for doc in result
    )

    assert trace.stages[0].stage_type == "batch"
    assert len(trace.stages[0].input_documents) == 2
    assert len(trace.stages[0].output_documents) == 2


def test_trace_preserves_input_snapshot_when_stage_mutates_document():

    document = Document(id="1", text="Original")

    pipeline = Pipeline([
        AppendTextStage(" Modified")
    ])

    _, trace = pipeline.run_with_trace(document)

    stage_trace = trace.stages[0]

    assert stage_trace.input_documents[0].text == "Original"
    assert stage_trace.output_documents[0].text == "Original Modified"


def test_trace_records_failed_stage():

    pipeline = Pipeline([
        FailingStage()
    ])

    document = Document(id="1", text="Hello")

    with pytest.raises(PipelineExecutionError) as exc_info:
        pipeline.run_with_trace(document)

    error = exc_info.value

    assert error.trace.stages[0].status == "failed"
    assert "ValueError" in error.trace.stages[0].error
    assert isinstance(error.original_error, ValueError)


def test_normal_execution_still_works():

    pipeline = Pipeline([
        AppendTextStage("!")
    ])

    result = pipeline.run(
        Document(id="1", text="Hello")
    )

    assert isinstance(result, list)
    assert result[0].text == "Hello!"

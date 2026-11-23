
import json

from llmforge.core.document import Document
from llmforge.core.pipeline import Pipeline
from llmforge.core.stage import ProcessingStage


class AppendTextStage(ProcessingStage):

    def process(self, document):
        document.text += "!"
        return document


def test_pipeline_trace_to_dict():

    pipeline = Pipeline([AppendTextStage()])

    _, trace = pipeline.run_with_trace(
        Document(
            id="1",
            text="سلام دنیا",
        )
    )

    result = trace.to_dict()

    assert result["input_count"] == 1
    assert result["output_count"] == 1
    assert len(result["stages"]) == 1

    assert (
        result["stages"][0]["input_documents"][0]["text"]
        == "سلام دنیا"
    )

    assert (
        result["stages"][0]["output_documents"][0]["text"]
        == "سلام دنیا!"
    )


def test_pipeline_trace_to_json():

    pipeline = Pipeline([AppendTextStage()])

    _, trace = pipeline.run_with_trace(
        Document(id="1", text="سلام")
    )

    json_output = trace.to_json()

    parsed = json.loads(json_output)

    assert parsed["input_count"] == 1
    assert parsed["output_count"] == 1

    # Persian characters should remain readable.
    assert "سلام" in json_output


def test_trace_json_contains_duration():

    pipeline = Pipeline([AppendTextStage()])

    _, trace = pipeline.run_with_trace(
        Document(id="1", text="Hello")
    )

    parsed = json.loads(trace.to_json())

    assert "total_duration_ms" in parsed
    assert "duration_ms" in parsed["stages"][0]

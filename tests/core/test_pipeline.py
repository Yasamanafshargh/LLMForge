
import pytest

from llmforge.core.document import Document
from llmforge.core.pipeline import Pipeline
from llmforge.core.stage import ProcessingStage
from llmforge.core.transform import DocumentTransform


class UppercaseStage(ProcessingStage):

    def process(self, document):
        document.text = document.text.upper()
        return document


class SplitTransform(DocumentTransform):

    def transform(self, document):
        parts = document.text.split("|")

        return [
            Document(
                id=f"{document.id}_{index}",
                text=part,
                metadata=document.metadata.copy()
            )
            for index, part in enumerate(parts)
        ]


def test_pipeline_with_processing_stage():
    document = Document(id="1", text="hello")

    pipeline = Pipeline([UppercaseStage()])
    results = pipeline.run(document)

    assert len(results) == 1
    assert results[0].text == "HELLO"


def test_pipeline_with_transform():
    document = Document(id="1", text="first|second|third")

    pipeline = Pipeline([SplitTransform()])
    results = pipeline.run(document)

    assert len(results) == 3
    assert results[0].text == "first"
    assert results[2].text == "third"


def test_pipeline_with_stage_and_transform():
    document = Document(id="1", text="hello|world")

    pipeline = Pipeline([
        UppercaseStage(),
        SplitTransform()
    ])

    results = pipeline.run(document)

    assert len(results) == 2
    assert results[0].text == "HELLO"
    assert results[1].text == "WORLD"


def test_pipeline_with_empty_transform():
    class EmptyTransform(DocumentTransform):

        def transform(self, document):
            return []

    document = Document(id="1", text="hello")

    pipeline = Pipeline([EmptyTransform()])
    results = pipeline.run(document)

    assert results == []


def test_pipeline_rejects_unsupported_stage():
    document = Document(id="1", text="hello")

    class InvalidStage:
        pass

    pipeline = Pipeline([InvalidStage()])

    with pytest.raises(TypeError):
        pipeline.run(document)

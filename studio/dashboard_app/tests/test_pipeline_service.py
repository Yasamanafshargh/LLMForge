
import pytest

from llmforge.core.pipeline import Pipeline
from llmforge.core.document import Document
from llmforge.core.stage import ProcessingStage
import json
from dashboard_app.models import Dataset
from dashboard_app.services.pipeline_service import PipelineService


class AppendTextStage(ProcessingStage):

    def process(self, document):
        document.text += "!"
        return document


@pytest.mark.django_db
def test_pipeline_service_executes_core_pipeline():

    dataset = Dataset.objects.create(
        name="Test Dataset",
        file_format="txt",
    )

    pipeline = Pipeline([
        AppendTextStage()
    ])

    documents = [
        Document(id="1", text="Hello"),
        Document(id="2", text="World"),
    ]

    service = PipelineService()

    result = service.execute(
        pipeline,
        documents,
        dataset,
        "Test Pipeline Experiment",
    )

    assert len(result["documents"]) == 2

    assert result["documents"][0]["text"] == "Hello!"
    assert result["documents"][1]["text"] == "World!"

    assert "stages" in result["trace"]
    assert len(result["trace"]["stages"]) == 1

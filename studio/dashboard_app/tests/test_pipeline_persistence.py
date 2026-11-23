
import pytest

from llmforge.core.pipeline import Pipeline
from llmforge.core.stage import ProcessingStage
from llmforge.core.document import Document

from dashboard_app.models import Dataset, Experiment, StageExecution
from dashboard_app.services.pipeline_service import PipelineService


class AppendTextStage(ProcessingStage):

    def process(self, document):
        document.text += "!"
        return document


class FailingStage(ProcessingStage):

    def process(self, document):
        raise ValueError("Intentional test failure")


@pytest.mark.django_db
def test_pipeline_service_saves_successful_experiment():

    dataset = Dataset.objects.create(
        name="Test Dataset",
        file_format="txt",
        document_count=2,
    )

    pipeline = Pipeline([
        AppendTextStage(),
    ])

    documents = [
        Document(id="1", text="Hello"),
        Document(id="2", text="World"),
    ]

    service = PipelineService()

    result = service.execute(
        pipeline=pipeline,
        documents=documents,
        dataset=dataset,
        experiment_name="Successful Experiment",
    )

    experiment = Experiment.objects.get(
        id=result["experiment_id"]
    )

    assert experiment.status == "completed"
    assert experiment.input_count == 2
    assert experiment.output_count == 2

    assert result["documents"][0]["text"] == "Hello!"

    stages = StageExecution.objects.filter(
        experiment=experiment
    )

    assert stages.count() == 1
    assert stages.first().stage_name == "AppendTextStage"


@pytest.mark.django_db
def test_pipeline_service_saves_failed_experiment():

    dataset = Dataset.objects.create(
        name="Failure Dataset",
        file_format="txt",
    )

    pipeline = Pipeline([
        FailingStage(),
    ])

    documents = [
        Document(id="1", text="Hello"),
    ]

    service = PipelineService()

    with pytest.raises(Exception):
        service.execute(
            pipeline=pipeline,
            documents=documents,
            dataset=dataset,
            experiment_name="Failed Experiment",
        )

    experiment = Experiment.objects.get(
        name="Failed Experiment"
    )

    assert experiment.status == "failed"

    failed_stage = StageExecution.objects.get(
        experiment=experiment
    )

    assert failed_stage.status == "failed"
    assert "ValueError" in failed_stage.error


@pytest.mark.django_db
def test_pipeline_service_preserves_successful_stages_before_failure():

    dataset = Dataset.objects.create(
        name="Partial Failure Dataset",
        file_format="txt",
    )

    pipeline = Pipeline([
        AppendTextStage(),
        FailingStage(),
    ])

    documents = [
        Document(id="1", text="Hello"),
    ]

    service = PipelineService()

    with pytest.raises(Exception):
        service.execute(
            pipeline=pipeline,
            documents=documents,
            dataset=dataset,
            experiment_name="Partial Failure Experiment",
        )

    experiment = Experiment.objects.get(
        name="Partial Failure Experiment"
    )

    stages = list(
        experiment.stage_executions.all()
    )

    assert experiment.status == "failed"
    assert len(stages) == 2

    assert stages[0].stage_name == "AppendTextStage"
    assert stages[0].status == "success"

    assert stages[1].stage_name == "FailingStage"
    assert stages[1].status == "failed"

    assert stages[0].output_documents[0]["text"] == "Hello!"
    assert "ValueError" in stages[1].error

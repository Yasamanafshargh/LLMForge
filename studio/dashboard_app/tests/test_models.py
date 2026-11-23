
import pytest
from django.db.models import ProtectedError

from dashboard_app.models import (
    Dataset,
    Experiment,
    StageExecution,
)


@pytest.mark.django_db
def test_dataset_creation():
    dataset = Dataset.objects.create(
        name="Persian Research Dataset",
        file_format="jsonl",
        document_count=100,
    )

    assert dataset.name == "Persian Research Dataset"
    assert dataset.file_format == "jsonl"
    assert dataset.document_count == 100


@pytest.mark.django_db
def test_experiment_creation():
    dataset = Dataset.objects.create(
        name="Research Dataset",
        file_format="txt",
    )

    experiment = Experiment.objects.create(
        name="First BPE Experiment",
        dataset=dataset,
        configuration={"vocab_size": 1000},
    )

    assert experiment.dataset == dataset
    assert experiment.status == "pending"
    assert experiment.configuration["vocab_size"] == 1000


@pytest.mark.django_db
def test_experiment_can_have_multiple_stage_executions():
    dataset = Dataset.objects.create(
        name="Test Dataset",
        file_format="json",
    )

    experiment = Experiment.objects.create(
        name="Pipeline Test",
        dataset=dataset,
    )

    StageExecution.objects.create(
        experiment=experiment,
        stage_name="Normalization",
        stage_type="processing",
        order=1,
    )

    StageExecution.objects.create(
        experiment=experiment,
        stage_name="Chunking",
        stage_type="transform",
        order=2,
    )

    stages = list(experiment.stage_executions.all())

    assert len(stages) == 2
    assert stages[0].stage_name == "Normalization"
    assert stages[1].stage_name == "Chunking"


@pytest.mark.django_db
def test_dataset_cannot_be_deleted_if_used_by_experiment():
    dataset = Dataset.objects.create(
        name="Protected Dataset",
        file_format="txt",
    )

    Experiment.objects.create(
        name="Experiment Using Dataset",
        dataset=dataset,
    )

    with pytest.raises(ProtectedError):
        dataset.delete()

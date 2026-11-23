
from django.db import models


class Dataset(models.Model):
    FORMAT_CHOICES = [
        ("txt", "Text"),
        ("json", "JSON"),
        ("jsonl", "JSONL"),
        ("csv", "CSV"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    source_file = models.FileField(
        upload_to="datasets/",
        blank=True,
        null=True,
    )

    file_format = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES,
    )

    document_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Experiment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    name = models.CharField(max_length=255)

    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.PROTECT,
        related_name="experiments",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    configuration = models.JSONField(default=dict, blank=True)

    input_count = models.PositiveIntegerField(default=0)
    output_count = models.PositiveIntegerField(default=0)

    total_duration_ms = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class StageExecution(models.Model):
    experiment = models.ForeignKey(
        Experiment,
        on_delete=models.CASCADE,
        related_name="stage_executions",
    )

    stage_name = models.CharField(max_length=255)
    stage_type = models.CharField(max_length=50)

    configuration = models.JSONField(default=dict, blank=True)

    input_documents = models.JSONField(default=list, blank=True)
    output_documents = models.JSONField(default=list, blank=True)

    duration_ms = models.FloatField(default=0)

    status = models.CharField(max_length=20, default="success")
    error = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.stage_name} - {self.experiment.name}"

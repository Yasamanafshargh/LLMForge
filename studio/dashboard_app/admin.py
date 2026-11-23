from django.contrib import admin
from .models import Dataset, Experiment, StageExecution


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("name", "file_format", "document_count", "created_at")
    search_fields = ("name",)
    list_filter = ("file_format",)


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "dataset",
        "status",
        "input_count",
        "output_count",
        "total_duration_ms",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("name",)


@admin.register(StageExecution)
class StageExecutionAdmin(admin.ModelAdmin):
    list_display = (
        "stage_name",
        "experiment",
        "stage_type",
        "status",
        "duration_ms",
        "order",
    )
    list_filter = ("stage_type", "status")
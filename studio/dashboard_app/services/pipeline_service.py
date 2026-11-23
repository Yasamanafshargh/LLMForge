
from django.utils import timezone
from django.db import transaction
from llmforge.core.pipeline import Pipeline, PipelineExecutionError
from llmforge.core.document import Document
import json
from dashboard_app.models import Experiment, StageExecution


class PipelineService:

    def execute(
        self,
        pipeline: Pipeline,
        documents: list[Document],
        dataset,
        experiment_name: str,
    ) -> dict:

        if not isinstance(pipeline, Pipeline):
            raise TypeError("pipeline must be a Pipeline instance.")

        if not isinstance(documents, list):
            raise TypeError("documents must be a list.")

        if dataset is None:
            raise ValueError("A dataset must be provided.")

        if not isinstance(experiment_name, str) or not experiment_name.strip():
            raise ValueError("experiment_name cannot be empty.")

        # Create an experiment record before execution.
        experiment = Experiment.objects.create(
            name=experiment_name.strip(),
            dataset=dataset,
            status="running",
            input_count=len(documents),
            configuration={
                "pipeline_stages": [
                    {
                        "name": stage.__class__.__name__,
                        "type": stage.__class__.__bases__[0].__name__,
                    }
                    for stage in pipeline.stages
                ]
            },
        )
        try:
            result, trace = pipeline.run_batch_with_trace(documents)

            # Save every stage execution.
            with transaction.atomic():

                stage_records = []

                for index, stage in enumerate(trace.stages):
                    stage_records.append(
                        StageExecution(
                            experiment=experiment,
                            stage_name=stage.stage_name,
                            stage_type=stage.stage_type,
                            configuration=json.loads(
                                json.dumps(stage.configuration, default=str)
                            ),
                            input_documents=[
                                doc.model_dump(mode="json")
                                for doc in stage.input_documents
                            ],
                            output_documents=[
                                doc.model_dump(mode="json")
                                for doc in stage.output_documents
                            ],
                            duration_ms=stage.duration_ms,
                            status=stage.status,
                            error=stage.error or "",
                            order=index,
                        )
                    )

                StageExecution.objects.bulk_create(stage_records)

                experiment.status = "completed"
                experiment.output_count = len(result)
                experiment.total_duration_ms = trace.total_duration_ms
                experiment.finished_at = timezone.now()
                experiment.save()

            return {
                "experiment_id": experiment.id,
                "documents": [
                    document.model_dump(mode="json")
                    for document in result
                ],
                "trace": trace.to_dict(),
            }

        except PipelineExecutionError as exc:
            # Preserve completed and failed stage information.
            with transaction.atomic():

                for index, stage in enumerate(exc.trace.stages):
                    StageExecution.objects.create(
                        experiment=experiment,
                        stage_name=stage.stage_name,
                        stage_type=stage.stage_type,
                        configuration=json.loads(
                            json.dumps(stage.configuration, default=str)
                        ),
                        input_documents=[
                            doc.model_dump(mode="json")
                            for doc in stage.input_documents
                        ],
                        output_documents=[
                            doc.model_dump(mode="json")
                            for doc in stage.output_documents
                        ],
                        duration_ms=stage.duration_ms,
                        status=stage.status,
                        error=stage.error or "",
                        order=index,
                    )

                experiment.status = "failed"
                experiment.total_duration_ms = exc.trace.total_duration_ms
                experiment.finished_at = timezone.now()
                experiment.save()
            raise

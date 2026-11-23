
from typing import Sequence, Any
from copy import deepcopy
from time import perf_counter

from llmforge.core.document import Document
from llmforge.core.stage import ProcessingStage
from llmforge.core.transform import DocumentTransform
from llmforge.batching.base_batch_stage import BatchProcessingStage
from llmforge.core.trace import (
    PipelineTrace,
    StageTrace,
    PipelineExecutionError,
)


class Pipeline:

    def __init__(
        self,
        stages: Sequence[
            ProcessingStage | DocumentTransform | BatchProcessingStage
        ],
    ):
        self.stages = list(stages)

    def run(self, document: Document) -> list[Document]:
        """Process a single document through the pipeline."""
        if not isinstance(document, Document):
            raise TypeError("Input must be a Document instance.")

        return self.run_batch([document])

    def run_batch(self, documents: list[Document]) -> list[Document]:
        """Process multiple documents through the pipeline."""
        result, _ = self._execute(documents, capture_trace=False)
        return result

    def run_with_trace(
        self,
        document: Document,
    ) -> tuple[list[Document], PipelineTrace]:
        """Process one document and capture execution details."""
        if not isinstance(document, Document):
            raise TypeError("Input must be a Document instance.")

        return self.run_batch_with_trace([document])

    def run_batch_with_trace(
        self,
        documents: list[Document],
    ) -> tuple[list[Document], PipelineTrace]:
        """Process multiple documents and capture execution details."""
        return self._execute(documents, capture_trace=True)

    def _execute(
        self,
        documents: list[Document],
        capture_trace: bool,
    ) -> tuple[list[Document], PipelineTrace]:

        if not isinstance(documents, list):
            raise TypeError("documents must be a list.")

        if not all(
            isinstance(document, Document)
            for document in documents
        ):
            raise TypeError("All items must be Document instances.")

        current_documents = documents.copy()

        trace = PipelineTrace(input_count=len(documents))

        for stage in self.stages:

            stage_name = type(stage).__name__
            stage_type = self._get_stage_type(stage)

            input_snapshot = (
                self._snapshot(current_documents)
                if capture_trace
                else []
            )

            configuration = (
                self._get_configuration(stage)
                if capture_trace
                else {}
            )

            start_time = perf_counter()

            try:
                current_documents = self._process_stage(
                    stage,
                    current_documents,
                )

            except Exception as exc:

                duration_ms = (
                    perf_counter() - start_time
                ) * 1000

                if capture_trace:
                    trace.stages.append(
                        StageTrace(
                            stage_name=stage_name,
                            stage_type=stage_type,
                            configuration=configuration,
                            input_documents=input_snapshot,
                            output_documents=[],
                            duration_ms=duration_ms,
                            status="failed",
                            error=f"{type(exc).__name__}: {exc}",
                        )
                    )

                    raise PipelineExecutionError(
                        f"Pipeline failed during stage '{stage_name}'.",
                        trace=trace,
                        original_error=exc,
                    ) from exc

                raise

            duration_ms = (
                perf_counter() - start_time
            ) * 1000

            if capture_trace:
                trace.stages.append(
                    StageTrace(
                        stage_name=stage_name,
                        stage_type=stage_type,
                        configuration=configuration,
                        input_documents=input_snapshot,
                        output_documents=self._snapshot(
                            current_documents
                        ),
                        duration_ms=duration_ms,
                    )
                )

        trace.output_count = len(current_documents)

        return current_documents, trace

    @staticmethod
    def _process_stage(
        stage: Any,
        documents: list[Document],
    ) -> list[Document]:

        if isinstance(stage, BatchProcessingStage):

            result = stage.process(documents)

            if not isinstance(result, list):
                raise TypeError(
                    "BatchProcessingStage must return a list."
                )

            if not all(
                isinstance(doc, Document) for doc in result
            ):
                raise TypeError(
                    "BatchProcessingStage must return Documents."
                )

            return result

        elif isinstance(stage, ProcessingStage):

            processed_documents = []

            for document in documents:
                result = stage.process(document)

                if not isinstance(result, Document):
                    raise TypeError(
                        "ProcessingStage must return a Document."
                    )

                processed_documents.append(result)

            return processed_documents

        elif isinstance(stage, DocumentTransform):

            transformed_documents = []

            for document in documents:
                result = stage.transform(document)

                if not isinstance(result, list):
                    raise TypeError(
                        "DocumentTransform must return a list."
                    )

                if not all(
                    isinstance(doc, Document) for doc in result
                ):
                    raise TypeError(
                        "DocumentTransform must return Documents."
                    )

                transformed_documents.extend(result)

            return transformed_documents

        raise TypeError(
            f"Unsupported pipeline stage: {type(stage).__name__}"
        )

    @staticmethod
    def _get_stage_type(stage: Any) -> str:

        if isinstance(stage, BatchProcessingStage):
            return "batch"

        if isinstance(stage, ProcessingStage):
            return "processing"

        if isinstance(stage, DocumentTransform):
            return "transform"

        return "unsupported"

    @staticmethod
    def _snapshot(
        documents: list[Document],
    ) -> list[Document]:
        return [
            document.model_copy(deep=True)
            for document in documents
        ]

    @staticmethod
    def _get_configuration(stage: Any) -> dict[str, Any]:

        configuration = {}

        for name, value in vars(stage).items():

            if name.startswith("_"):
                continue

            try:
                configuration[name] = deepcopy(value)
            except Exception:
                configuration[name] = repr(value)

        return configuration

import json
from dataclasses import dataclass, field
from typing import Any

from llmforge.core.document import Document


@dataclass
class StageTrace:
    stage_name: str
    stage_type: str
    configuration: dict[str, Any]

    input_documents: list[Document]
    output_documents: list[Document]

    duration_ms: float

    status: str = "success"
    error: str | None = None


    def to_dict(self) -> dict[str, Any]:
        return {
            "stage_name": self.stage_name,
            "stage_type": self.stage_type,
            "configuration": self.configuration,
            "input_documents": [
                document.model_dump(mode="json")
                for document in self.input_documents
            ],
            "output_documents": [
                document.model_dump(mode="json")
                for document in self.output_documents
            ],
            "duration_ms": self.duration_ms,
            "status": self.status,
            "error": self.error,
        }


@dataclass
class PipelineTrace:
    stages: list[StageTrace] = field(default_factory=list)

    input_count: int = 0
    output_count: int = 0

    @property
    def total_duration_ms(self) -> float:
        return sum(stage.duration_ms for stage in self.stages)


    def to_dict(self) -> dict[str, Any]:
        return {
            "input_count": self.input_count,
            "output_count": self.output_count,
            "total_duration_ms": self.total_duration_ms,
            "stages": [
                stage.to_dict()
                for stage in self.stages
            ],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
            indent=indent,
        )

class PipelineExecutionError(RuntimeError):
    """Raised when a pipeline stage fails during traced execution."""

    def __init__(
        self,
        message: str,
        trace: PipelineTrace,
        original_error: Exception,
    ):
        super().__init__(message)
        self.trace = trace
        self.original_error = original_error

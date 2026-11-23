
from abc import ABC, abstractmethod

from llmforge.core.document import Document


class BatchProcessingStage(ABC):

    @abstractmethod
    def process(
        self,
        documents: list[Document]
    ) -> list[Document]:
        pass

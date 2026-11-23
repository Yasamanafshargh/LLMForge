from abc import ABC, abstractmethod

from llmforge.core.document import Document


class ProcessingStage(ABC):

    @abstractmethod
    def process(self, document: Document) -> Document:
        pass
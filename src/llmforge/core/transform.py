
from abc import ABC, abstractmethod
from llmforge.core.document import Document


class DocumentTransform(ABC):

    @abstractmethod
    def transform(self, document: Document) -> list[Document]:
        pass

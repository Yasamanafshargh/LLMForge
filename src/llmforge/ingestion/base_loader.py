from abc import ABC, abstractmethod

from llmforge.core.document import Document


class BaseLoader(ABC):

    @abstractmethod
    def load(self, source: str) -> list[Document]:
        pass
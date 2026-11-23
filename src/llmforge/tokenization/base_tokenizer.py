from abc import ABC, abstractmethod


class BaseTokenizer(ABC):

    @abstractmethod
    def tokenize(self, text: str) -> list[str]:
        pass
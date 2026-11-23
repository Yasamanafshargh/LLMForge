
import random

from llmforge.core.document import Document


class DatasetSplitter:
    def __init__(
        self,
        train_ratio: float = 0.8,
        validation_ratio: float = 0.1,
        test_ratio: float = 0.1,
        shuffle: bool = True,
        seed: int | None = 42,
    ):
        ratios = [train_ratio, validation_ratio, test_ratio]

        if any(
            isinstance(ratio, bool)
            or not isinstance(ratio, (int, float))
            or ratio < 0
            for ratio in ratios
        ):
            raise ValueError("Split ratios must be non-negative numbers.")

        if not 0 < train_ratio <= 1:
            raise ValueError("train_ratio must be greater than 0 and at most 1.")

        if not abs(sum(ratios) - 1.0) < 1e-9:
            raise ValueError("Split ratios must add up to 1.0.")

        if not isinstance(shuffle, bool):
            raise TypeError("shuffle must be a boolean.")

        if seed is not None and (
            isinstance(seed, bool) or not isinstance(seed, int)
        ):
            raise TypeError("seed must be an integer or None.")

        self.train_ratio = train_ratio
        self.validation_ratio = validation_ratio
        self.test_ratio = test_ratio
        self.shuffle = shuffle
        self.seed = seed

    def split(self, documents: list[Document]) -> dict[str, list[Document]]:
        if not isinstance(documents, list):
            raise TypeError("documents must be a list.")

        if not all(isinstance(doc, Document) for doc in documents):
            raise TypeError("All items must be Document instances.")

        document_ids = [doc.id for doc in documents]

        if len(document_ids) != len(set(document_ids)):
            raise ValueError("Document IDs must be unique.")

        items = documents.copy()

        if self.shuffle:
            random.Random(self.seed).shuffle(items)

        train_end = int(len(items) * self.train_ratio)
        validation_end = int(
            len(items) * (self.train_ratio + self.validation_ratio)
        )

        return {
            "train": items[:train_end],
            "validation": items[train_end:validation_end],
            "test": items[validation_end:],
        }

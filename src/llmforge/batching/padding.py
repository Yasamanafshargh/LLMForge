
from llmforge.core.document import Document
from llmforge.batching.base_batch_stage import BatchProcessingStage


class PaddingStage(BatchProcessingStage):

    def __init__(
        self,
        pad_token_id: int = 0,
        max_length: int | None = None,
        padding: bool = True,
        truncation: bool = False,
    ):
        if not isinstance(pad_token_id, int) or pad_token_id < 0:
            raise ValueError("pad_token_id must be a non-negative integer.")

        if max_length is not None and max_length < 1:
            raise ValueError("max_length must be at least 1.")

        if not isinstance(padding, bool):
            raise TypeError("padding must be a boolean.")

        if not isinstance(truncation, bool):
            raise TypeError("truncation must be a boolean.")

        if max_length is not None and not truncation:
            raise ValueError(
                "A fixed max_length requires truncation=True "
                "to handle sequences that exceed it."
            )

        self.pad_token_id = pad_token_id
        self.max_length = max_length
        self.padding = padding
        self.truncation = truncation

    def process(
        self,
        documents: list[Document]
    ) -> list[Document]:

        if not isinstance(documents, list):
            raise TypeError("documents must be a list.")

        if not all(isinstance(doc, Document) for doc in documents):
            raise TypeError("All items must be Document instances.")

        if not documents:
            return []

        sequences = [doc.token_ids.copy() for doc in documents]

        for sequence in sequences:
            if not all(
                isinstance(token_id, int) and token_id >= 0
                for token_id in sequence
            ):
                raise ValueError(
                    "Token IDs must be non-negative integers."
                )

        if self.truncation and self.max_length is not None:
            sequences = [
                sequence[:self.max_length]
                for sequence in sequences
            ]

        if self.padding:
            target_length = (
                self.max_length
                if self.max_length is not None
                else max(len(sequence) for sequence in sequences)
            )

            for sequence in sequences:
                if len(sequence) > target_length:
                    raise ValueError(
                        "Sequence exceeds target length. "
                        "Enable truncation or increase max_length."
                    )
        else:
            target_length = None

        for document, sequence in zip(documents, sequences):

            attention_mask = [1] * len(sequence)

            if self.padding:
                padding_length = target_length - len(sequence)

                sequence.extend(
                    [self.pad_token_id] * padding_length
                )

                attention_mask.extend([0] * padding_length)

            document.token_ids = sequence
            document.metadata["attention_mask"] = attention_mask

        return documents

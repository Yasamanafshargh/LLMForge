
from dataclasses import dataclass

from llmforge.core.document import Document


@dataclass
class TrainingExample:
    document_id: str
    input_ids: list[int]
    target_ids: list[int]


class SequenceBuilder:
    def build(
        self,
        documents: list[Document],
    ) -> list[TrainingExample]:

        if not isinstance(documents, list):
            raise TypeError("documents must be a list.")

        if not all(isinstance(doc, Document) for doc in documents):
            raise TypeError("All items must be Document instances.")

        examples = []

        for document in documents:
            token_ids = document.token_ids

            if not isinstance(token_ids, list):
                raise TypeError(
                    f"Token IDs for document {document.id} must be a list."
                )

            if not all(
                isinstance(token_id, int)
                and not isinstance(token_id, bool)
                and token_id >= 0
                for token_id in token_ids
            ):
                raise ValueError(
                    f"Invalid token IDs in document {document.id}."
                )

            if len(token_ids) < 2:
                raise ValueError(
                    f"Document {document.id} must contain "
                    "at least two token IDs."
                )

            input_ids = token_ids[:-1]
            target_ids = token_ids[1:]

            examples.append(
                TrainingExample(
                    document_id=document.id,
                    input_ids=input_ids,
                    target_ids=target_ids,
                )
            )

        return examples

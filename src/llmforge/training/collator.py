
from dataclasses import dataclass

from llmforge.training.sequence_builder import TrainingExample


@dataclass
class TrainingBatch:
    document_ids: list[str]
    input_ids: list[list[int]]
    target_ids: list[list[int]]
    attention_mask: list[list[int]]


class CausalLMCollator:
    def __init__(
        self,
        pad_token_id: int = 0,
        ignore_index: int = -100,
    ):
        if (
            not isinstance(pad_token_id, int)
            or isinstance(pad_token_id, bool)
            or pad_token_id < 0
        ):
            raise ValueError("pad_token_id must be a non-negative integer.")

        if (
            not isinstance(ignore_index, int)
            or isinstance(ignore_index, bool)
        ):
            raise TypeError("ignore_index must be an integer.")

        self.pad_token_id = pad_token_id
        self.ignore_index = ignore_index

    def __call__(
        self,
        examples: list[TrainingExample],
    ) -> TrainingBatch:

        if not isinstance(examples, list):
            raise TypeError("examples must be a list.")

        if not all(
            isinstance(example, TrainingExample)
            for example in examples
        ):
            raise TypeError(
                "All items must be TrainingExample instances."
            )

        if not examples:
            return TrainingBatch(
                document_ids=[],
                input_ids=[],
                target_ids=[],
                attention_mask=[],
            )

        max_length = 0

        for example in examples:
            if not isinstance(example.input_ids, list):
                raise TypeError("input_ids must be a list.")

            if not isinstance(example.target_ids, list):
                raise TypeError("target_ids must be a list.")

            if len(example.input_ids) != len(example.target_ids):
                raise ValueError(
                    f"Input and target lengths must match "
                    f"for document {example.document_id}."
                )

            if not example.input_ids:
                raise ValueError(
                    f"Training example {example.document_id} is empty."
                )

            for token_id in example.input_ids + example.target_ids:
                if (
                    not isinstance(token_id, int)
                    or isinstance(token_id, bool)
                    or token_id < 0
                ):
                    raise ValueError(
                        f"Invalid token ID in document "
                        f"{example.document_id}."
                    )

            max_length = max(max_length, len(example.input_ids))

        batch_input_ids = []
        batch_target_ids = []
        batch_attention_mask = []
        document_ids = []

        for example in examples:
            input_padding = max_length - len(example.input_ids)

            padded_inputs = (
                example.input_ids.copy()
                + [self.pad_token_id] * input_padding
            )

            padded_targets = (
                example.target_ids.copy()
                + [self.ignore_index] * input_padding
            )

            attention_mask = (
                [1] * len(example.input_ids)
                + [0] * input_padding
            )

            document_ids.append(example.document_id)
            batch_input_ids.append(padded_inputs)
            batch_target_ids.append(padded_targets)
            batch_attention_mask.append(attention_mask)

        return TrainingBatch(
            document_ids=document_ids,
            input_ids=batch_input_ids,
            target_ids=batch_target_ids,
            attention_mask=batch_attention_mask,
        )

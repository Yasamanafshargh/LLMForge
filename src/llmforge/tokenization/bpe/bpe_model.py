
from pydantic import BaseModel, Field, model_validator


class BPEModel(BaseModel):

    merges: list[tuple[str, str]] = Field(default_factory=list)

    vocabulary: list[str] = Field(default_factory=list)

    special_tokens: list[str] = Field(
        default_factory=lambda: [
            "[PAD]",
            "[UNK]",
            "[BOS]",
            "[EOS]"
        ]
    )

    config: dict = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_model(self):

        if len(set(self.special_tokens)) != len(self.special_tokens):
            raise ValueError("Special tokens must be unique.")

        if len(set(self.vocabulary)) != len(self.vocabulary):
            raise ValueError("Vocabulary tokens must be unique.")

        if not all(
            isinstance(token, str) for token in self.vocabulary
        ):
            raise ValueError("Vocabulary entries must be strings.")

        for pair in self.merges:
            if len(pair) != 2:
                raise ValueError("Each merge rule must contain two tokens.")

            if not all(isinstance(token, str) for token in pair):
                raise ValueError("Merge rule elements must be strings.")

        return self

    def save(self, path: str):

        with open(path, "w", encoding="utf-8") as file:
            file.write(
                self.model_dump_json(indent=4)
            )

    @classmethod
    def load(cls, path: str):

        with open(path, "r", encoding="utf-8") as file:
            return cls.model_validate_json(file.read())

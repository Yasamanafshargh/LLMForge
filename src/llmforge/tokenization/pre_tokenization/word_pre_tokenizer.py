
import re
from dataclasses import dataclass


@dataclass
class PreTokenizationResult:
    tokens: list[str]
    separators: list[str]

    def __post_init__(self):
        if len(self.separators) != len(self.tokens) + 1:
            raise ValueError(
                "There must be exactly one more separator than tokens."
            )

    def reconstruct(self) -> str:
        parts = []

        for index, token in enumerate(self.tokens):
            parts.append(self.separators[index])
            parts.append(token)

        parts.append(self.separators[-1])

        return "".join(parts)


class WordPreTokenizer:

    TOKEN_PATTERN = re.compile(
        r"[^\W\d_]+(?:\u200c[^\W\d_]+)*"
        r"|\d+(?:[.,٫]\d+)?"
        r"|[^\w\s]",
        re.UNICODE
    )

    def pre_tokenize(self, text: str) -> PreTokenizationResult:

        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        tokens = []
        separators = []

        cursor = 0

        for match in self.TOKEN_PATTERN.finditer(text):
            separators.append(text[cursor:match.start()])
            tokens.append(match.group())

            cursor = match.end()

        # Preserve any whitespace or other characters after the last token.
        separators.append(text[cursor:])

        return PreTokenizationResult(
            tokens=tokens,
            separators=separators
        )

    def tokenize(self, text: str) -> list[str]:
        return self.pre_tokenize(text).tokens

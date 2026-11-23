import re

from llmforge.tokenization.base_tokenizer import BaseTokenizer


class BasicTokenizer(BaseTokenizer):

    TOKEN_PATTERN = re.compile(
        r"\d+(?:[.,٫]\d+)?|[^\W\d_]+(?:\u200c[^\W\d_]+)*|[^\w\s]"
    )

    def tokenize(self, text: str) -> list[str]:

        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        return self.TOKEN_PATTERN.findall(text)
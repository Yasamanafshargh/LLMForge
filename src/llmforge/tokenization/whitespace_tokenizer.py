from llmforge.tokenization.base_tokenizer import BaseTokenizer


class WhitespaceTokenizer(BaseTokenizer):

    def tokenize(self, text: str) -> list[str]:

        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        return text.split()
from llmforge.tokenization.bpe.bpe_model import BPEModel
from llmforge.tokenization.base_tokenizer import BaseTokenizer
from llmforge.tokenization.pre_tokenization import (
    WordPreTokenizer,
    PreTokenizationResult
)


class BPETokenizer(BaseTokenizer):

    def __init__(self, merges, pre_tokenizer=None):
        self.merges = list(merges)

        self.pre_tokenizer = (
            pre_tokenizer
            if pre_tokenizer is not None
            else WordPreTokenizer()
        )

    def apply_merges(self, symbols: list[str]) -> list[str]:

        for pair in self.merges:
            merged_symbols = []
            index = 0

            while index < len(symbols):

                if (
                    index < len(symbols) - 1
                    and (symbols[index], symbols[index + 1]) == pair
                ):
                    merged_symbols.append(
                        symbols[index] + symbols[index + 1]
                    )
                    index += 2

                else:
                    merged_symbols.append(symbols[index])
                    index += 1

            symbols = merged_symbols

        return symbols

    def tokenize(self, text: str) -> list[str]:

        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        result = self.pre_tokenizer.pre_tokenize(text)

        subword_tokens = []

        for token in result.tokens:
            symbols = list(token)
            merged = self.apply_merges(symbols)
            subword_tokens.extend(merged)

        return subword_tokens

    def tokenize_with_spacing(
        self,
        text: str
    ) -> PreTokenizationResult:

        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        result = self.pre_tokenizer.pre_tokenize(text)

        subword_tokens = []
        separators = []

        for index, token in enumerate(result.tokens):

            # Preserve the separator before the original word.
            separators.append(result.separators[index])

            symbols = self.apply_merges(list(token))

            for subword_index, subword in enumerate(symbols):

                subword_tokens.append(subword)

                # Subwords from the same word have no separator.
                if subword_index < len(symbols) - 1:
                    separators.append("")

        # Preserve trailing whitespace.
        separators.append(result.separators[-1])

        return PreTokenizationResult(
            tokens=subword_tokens,
            separators=separators
        )

    @classmethod
    def from_model(cls, model: BPEModel, pre_tokenizer=None):
        if not isinstance(model, BPEModel):
            raise TypeError("model must be a BPEModel instance.")

        return cls(
            merges=model.merges,
            pre_tokenizer=pre_tokenizer
        )

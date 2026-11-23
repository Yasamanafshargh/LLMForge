
from collections import Counter
from dataclasses import dataclass

from llmforge.tokenization.basic_tokenizer import BasicTokenizer
from llmforge.stopwords.dictionaries import (
    ENGLISH_STOP_WORDS,
    PERSIAN_STOP_WORDS,
)


@dataclass
class StopWordAnalysis:
    total_tokens: int
    stop_word_count: int
    stop_word_percentage: float
    frequencies: dict[str, int]
    matched_words: list[str]


class StopWordAnalyzer:

    LANGUAGE_DICTIONARIES = {
        "english": ENGLISH_STOP_WORDS,
        "persian": PERSIAN_STOP_WORDS,
    }

    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer or BasicTokenizer()

    def analyze(
        self,
        text: str,
        languages: tuple[str, ...] = ("english", "persian"),
    ) -> StopWordAnalysis:

        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        stop_words = set()

        for language in languages:
            if language not in self.LANGUAGE_DICTIONARIES:
                raise ValueError(
                    f"Unsupported language: {language}"
                )

            stop_words.update(
                self.LANGUAGE_DICTIONARIES[language]
            )

        tokens = self.tokenizer.tokenize(text)

        # Count only word tokens, not punctuation or numbers.
        word_tokens = [
            token
            for token in tokens
            if token
            and any(char.isalpha() for char in token)
            and all(
                char.isalpha() or char == "\u200c"
                for char in token
            )
        ]

        matched_words = [
            token
            for token in word_tokens
            if token.casefold() in stop_words
        ]

        frequencies = Counter(
            token.casefold()
            for token in matched_words
        )

        total_tokens = len(word_tokens)
        stop_word_count = len(matched_words)

        percentage = (
            (stop_word_count / total_tokens) * 100
            if total_tokens > 0
            else 0.0
        )

        return StopWordAnalysis(
            total_tokens=total_tokens,
            stop_word_count=stop_word_count,
            stop_word_percentage=round(percentage, 2),
            frequencies=dict(frequencies),
            matched_words=matched_words,
        )

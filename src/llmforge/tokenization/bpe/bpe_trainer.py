
from collections import Counter
from llmforge.tokenization.bpe.bpe_model import BPEModel
from llmforge.tokenization.pre_tokenization import WordPreTokenizer


class BPETrainer:

    def __init__(self, pre_tokenizer=None):
        self.pre_tokenizer = (
            pre_tokenizer
            if pre_tokenizer is not None
            else WordPreTokenizer()
        )

        self.merges = []
        self.tokenized_corpus = []

    def count_pairs(self, corpus: list[list[str]]) -> Counter:
        pair_counts = Counter()

        for symbols in corpus:
            for index in range(len(symbols) - 1):
                pair = (symbols[index], symbols[index + 1])
                pair_counts[pair] += 1

        return pair_counts

    def merge_pair(
        self,
        symbols: list[str],
        pair: tuple[str, str]
    ) -> list[str]:

        merged = []
        index = 0

        while index < len(symbols):

            if (
                index < len(symbols) - 1
                and (symbols[index], symbols[index + 1]) == pair
            ):
                merged.append(symbols[index] + symbols[index + 1])
                index += 2

            else:
                merged.append(symbols[index])
                index += 1

        return merged

    def merge_corpus(
        self,
        corpus: list[list[str]],
        pair: tuple[str, str]
    ) -> list[list[str]]:

        return [
            self.merge_pair(symbols, pair)
            for symbols in corpus
        ]

    def train(
        self,
        corpus: list[str],
        num_merges: int
    ) -> list[tuple[str, str]]:

        if num_merges < 0:
            raise ValueError("num_merges must be non-negative.")

        if not all(isinstance(text, str) for text in corpus):
            raise TypeError("All corpus entries must be strings.")

        # Step 1: Pre-tokenize each text.
        # Step 2: Convert each pre-token into characters.
        tokenized_corpus = []

        for text in corpus:
            result = self.pre_tokenizer.pre_tokenize(text)

            for token in result.tokens:
                tokenized_corpus.append(list(token))

                # Store the initial character vocabulary before merging.
        self.initial_vocabulary = list(
            dict.fromkeys(
                symbol
                for sequence in tokenized_corpus
                for symbol in sequence
            )
        )

        self.merges = []

        # Learn the most frequent adjacent pairs.
        for _ in range(num_merges):

            pair_counts = self.count_pairs(tokenized_corpus)

            if not pair_counts:
                break

            best_pair = pair_counts.most_common(1)[0][0]

            tokenized_corpus = self.merge_corpus(
                tokenized_corpus,
                best_pair
            )

            self.merges.append(best_pair)

            print(
                f"Merged {best_pair} -> "
                f"{best_pair[0] + best_pair[1]}"
            )

        self.tokenized_corpus = tokenized_corpus

        return self.merges


    
    def build_model(self, config=None, special_tokens=None) -> BPEModel:

        if not self.initial_vocabulary:
            raise RuntimeError(
                "Train the BPE model before building it."
            )

        if special_tokens is None:
            special_tokens = [
                "[PAD]",
                "[UNK]",
                "[BOS]",
                "[EOS]"
            ]

        # Start with the initial character vocabulary.
        vocabulary = self.initial_vocabulary.copy()

        # Add every token created by a merge.
        for left, right in self.merges:
            merged_token = left + right

            if merged_token not in vocabulary:
                vocabulary.append(merged_token)

        # Add special tokens at the beginning.
        vocabulary = list(special_tokens) + [
            token for token in vocabulary
            if token not in special_tokens
        ]

        return BPEModel(
            merges=self.merges,
            vocabulary=vocabulary,
            special_tokens=special_tokens,
            config=config or {}
        )

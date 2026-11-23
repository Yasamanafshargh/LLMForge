
class Vocabulary:

    DEFAULT_SPECIAL_TOKENS = [
        "[PAD]",
        "[UNK]",
        "[BOS]",
        "[EOS]"
    ]

    def __init__(self, special_tokens=None):

        self.special_tokens = (
            self.DEFAULT_SPECIAL_TOKENS.copy()
            if special_tokens is None
            else list(special_tokens)
        )

        if len(set(self.special_tokens)) != len(self.special_tokens):
            raise ValueError("Special tokens must be unique.")

        self.token_to_id = {}
        self.id_to_token = {}

    def build(self, tokens):

        if not all(isinstance(token, str) for token in tokens):
            raise TypeError("All vocabulary tokens must be strings.")

        unique_tokens = list(dict.fromkeys(tokens))

        all_tokens = self.special_tokens + [
            token for token in unique_tokens
            if token not in self.special_tokens
        ]

        self.token_to_id = {
            token: index
            for index, token in enumerate(all_tokens)
        }

        self.id_to_token = {
            index: token
            for token, index in self.token_to_id.items()
        }

    def encode(self, tokens, add_bos=False, add_eos=False):

        if not self.token_to_id:
            raise RuntimeError("Vocabulary has not been built.")

        if not all(isinstance(token, str) for token in tokens):
            raise TypeError("All input tokens must be strings.")

        unknown_id = self.token_to_id["[UNK]"]

        token_ids = [
            self.token_to_id.get(token, unknown_id)
            for token in tokens
        ]

        if add_bos:
            token_ids.insert(0, self.token_to_id["[BOS]"])

        if add_eos:
            token_ids.append(self.token_to_id["[EOS]"])

        return token_ids

    def decode(self, token_ids):

        if not self.id_to_token:
            raise RuntimeError("Vocabulary has not been built.")

        decoded_tokens = []

        for token_id in token_ids:

            if not isinstance(token_id, int):
                raise TypeError("Token IDs must be integers.")

            if token_id not in self.id_to_token:
                raise ValueError(f"Invalid token ID: {token_id}")

            decoded_tokens.append(self.id_to_token[token_id])

        return decoded_tokens

    def __len__(self):

        return len(self.token_to_id)

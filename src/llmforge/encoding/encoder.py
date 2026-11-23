
from llmforge.core.document import Document
from llmforge.core.stage import ProcessingStage
from llmforge.tokenization.base_tokenizer import BaseTokenizer
from llmforge.tokenization.vocabulary import Vocabulary


class TokenEncodingStage(ProcessingStage):

    def __init__(
        self,
        tokenizer: BaseTokenizer,
        vocabulary: Vocabulary,
        add_bos: bool = False,
        add_eos: bool = False,
    ):
        self.tokenizer = tokenizer
        self.vocabulary = vocabulary
        self.add_bos = add_bos
        self.add_eos = add_eos

    def process(self, document: Document) -> Document:

        if not isinstance(document, Document):
            raise TypeError("Input must be a Document instance.")

        # Step 1: Convert text into tokens
        tokens = self.tokenizer.tokenize(document.text)

        # Step 2: Convert tokens into numerical IDs
        token_ids = self.vocabulary.encode(
            tokens,
            add_bos=self.add_bos,
            add_eos=self.add_eos,
        )

        # Step 3: Store the results in the document
        document.tokens = tokens
        document.token_ids = token_ids

        return document

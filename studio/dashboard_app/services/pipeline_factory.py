from llmforge.core.pipeline import Pipeline
from llmforge.cleaning.persian_stage import PersianNormalizationStage
from llmforge.chunking.sentence_transform import SentenceChunkTransform
from llmforge.tokenization.basic_tokenizer import BasicTokenizer
from llmforge.encoding.encoder import TokenEncodingStage
from llmforge.tokenization.vocabulary import Vocabulary


class PipelineFactory:

    @staticmethod
    def create(pipeline_type, documents=None):

        if pipeline_type == "normalization":
            return Pipeline([
                PersianNormalizationStage()
            ])

        if pipeline_type == "normalization_chunking":
            return Pipeline([
                PersianNormalizationStage(),
                SentenceChunkTransform(),
            ])

        if pipeline_type == "full_preprocessing":

            if documents is None:
                raise ValueError(
                    "Documents are required to build the vocabulary."
                )

            tokenizer = BasicTokenizer()
            vocabulary = Vocabulary()

            # Normalize documents before building the vocabulary.
            normalizer = PersianNormalizationStage()

            all_tokens = []

            for document in documents:
                normalized_document = normalizer.process(
                    document.model_copy(deep=True)
                )
                all_tokens.extend(
                    tokenizer.tokenize(normalized_document.text)
                )

            # Build vocabulary before numerical encoding.
            vocabulary.build(all_tokens)

            return Pipeline([
                PersianNormalizationStage(),
                SentenceChunkTransform(),
                TokenEncodingStage(
                    tokenizer=tokenizer,
                    vocabulary=vocabulary,
                ),
            ])

        raise ValueError(f"Unknown pipeline type: {pipeline_type}")
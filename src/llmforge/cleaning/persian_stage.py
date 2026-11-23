
from llmforge.core.document import Document
from llmforge.core.stage import ProcessingStage
from llmforge.cleaning.persian_normalizer import PersianNormalizer


class PersianNormalizationStage(ProcessingStage):

    def __init__(self, normalizer: PersianNormalizer | None = None):
        self.normalizer = normalizer or PersianNormalizer()

    def process(self, document: Document) -> Document:
        document.text = self.normalizer.normalize(document.text)
        return document

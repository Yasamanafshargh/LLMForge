from llmforge.core.document import Document
from llmforge.core.pipeline import Pipeline
from llmforge.cleaning.persian_stage import PersianNormalizationStage
from llmforge.chunking.sentence_transform import SentenceChunkTransform


document = Document(
    id="sample_1",
    text="یادگیری ماشین یکی از شاخه های هوش مصنوعی است. "
         "مدل های زبانی بزرگ می توانند متن تولید کنند."
)

pipeline = Pipeline([
    PersianNormalizationStage(),
    SentenceChunkTransform(sentences_per_chunk=1)
])

results = pipeline.run(document)

for result in results:
    print(f"ID: {result.id}")
    print(f"Text: {result.text}")
    print(f"Metadata: {result.metadata}")
    print("-" * 40)
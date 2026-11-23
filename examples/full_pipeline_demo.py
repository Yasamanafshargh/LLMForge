
from llmforge.ingestion import JSONLoader
from llmforge.core.pipeline import Pipeline
from llmforge.cleaning import PersianNormalizationStage
from llmforge.chunking import SentenceChunkTransform


# 1. Load documents
loader = JSONLoader(text_field="text")
documents = loader.load("data/raw/persian_dataset.json")


# 2. Build pipeline
pipeline = Pipeline([
    PersianNormalizationStage(),
    SentenceChunkTransform(sentences_per_chunk=2)
])


# 3. Process all documents
all_chunks = []

for document in documents:
    chunks = pipeline.run(document)
    all_chunks.extend(chunks)


# 4. Display results
print(f"Original documents: {len(documents)}")
print(f"Generated chunks: {len(all_chunks)}")

for chunk in all_chunks:
    print("\nID:", chunk.id)
    print("Text:", chunk.text)
    print("Metadata:", chunk.metadata)

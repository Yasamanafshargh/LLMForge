from llmforge.core.document import Document
from llmforge.cleaning.persian_stage import PersianNormalizationStage
from llmforge.chunking.sentence_transform import SentenceChunkTransform


document = Document(
    id="test_001",
    text="سلام   دنیا. این یک آزمایش است.",
    metadata={"category": "test"}
)

normalizer = PersianNormalizationStage()
chunk_transform = SentenceChunkTransform(
    sentences_per_chunk=1
)

# Step 1: Normalize
normalizer.process(document)

print("NORMALIZED DOCUMENT")
print(repr(document.text))

# Step 2: Chunk
chunks = chunk_transform.transform(document)

print("\nGENERATED CHUNKS")

for chunk in chunks:
    print("ID:", chunk.id)
    print("Text:", repr(chunk.text))
    print("Metadata:", chunk.metadata)

# Step 3: Verify original document
print("\nORIGINAL DOCUMENT AFTER CHUNKING")
print("ID:", document.id)
print("Text:", repr(document.text))
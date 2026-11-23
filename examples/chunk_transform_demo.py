
from llmforge.core.document import Document
from llmforge.chunking import SentenceChunkTransform

document = Document(
    id="ml_intro",
    text=(
        "یادگیری ماشین یکی از شاخه‌های هوش مصنوعی است. "
        "شبکه‌های عصبی در یادگیری عمیق استفاده می‌شوند. "
        "پردازش زبان طبیعی به درک زبان انسان کمک می‌کند."
    ),
    metadata={
        "category": "machine_learning",
        "language": "fa"
    }
)

transform = SentenceChunkTransform(
    sentences_per_chunk=1
)

chunks = transform.transform(document)

for chunk in chunks:
    print("\nID:", chunk.id)
    print("Text:", chunk.text)
    print("Metadata:", chunk.metadata)

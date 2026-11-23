
from llmforge.ingestion import JSONLoader

loader = JSONLoader()

documents = loader.load(
    "data/raw/persian_dataset.json"
)

for document in documents:
    print("=" * 50)
    print("ID:", document.id)
    print("Text:", document.text)
    print("Metadata:", document.metadata)

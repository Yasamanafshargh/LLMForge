from llmforge.ingestion import JSONLLoader

loader = JSONLLoader()

documents = loader.load(
    "data/raw/persian_dataset.jsonl"
)

for document in documents:
    print("=" * 50)
    print("ID:", document.id)
    print("Text:", document.text)
    print("Metadata:", document.metadata)
from llmforge.ingestion import CSVLoader

loader = CSVLoader(text_field="answer")

documents = loader.load(
    "data/raw/persian_dataset.csv"
)

for document in documents:
    print("=" * 50)
    print("ID:", document.id)
    print("Text:", document.text)
    print("Metadata:", document.metadata)
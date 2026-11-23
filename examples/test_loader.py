from llmforge.ingestion import TXTLoader


loader = TXTLoader()

documents = loader.load(
    "data/raw/sample.txt"
)

for document in documents:

    print("Document ID:", document.id)

    print("Text:")
    print(document.text)

    print("Metadata:")
    print(document.metadata)
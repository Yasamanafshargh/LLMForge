
from llmforge.core.document import Document
from llmforge.core.transform import DocumentTransform
from llmforge.chunking.sentence_chunker import SentenceChunker


class SentenceChunkTransform(DocumentTransform):

    def __init__(self, sentences_per_chunk: int = 3):
        self.chunker = SentenceChunker(
            sentences_per_chunk=sentences_per_chunk
        )

    def transform(self, document: Document) -> list[Document]:

        chunks = self.chunker.chunk(document.text)

        transformed_documents = []

        for index, chunk in enumerate(chunks):

            chunk_document = Document(
                id=f"{document.id}_chunk_{index}",
                text=chunk,
                metadata={
                    **document.metadata,
                    "parent_document_id": document.id,
                    "chunk_index": index,
                    "total_chunks": len(chunks),
                }
            )

            transformed_documents.append(chunk_document)

        return transformed_documents


import re


class SentenceChunker:

    def __init__(self, sentences_per_chunk: int = 3):
        if sentences_per_chunk < 1:
            raise ValueError("sentences_per_chunk must be at least 1")

        self.sentences_per_chunk = sentences_per_chunk

    def chunk(self, text: str) -> list[str]:

        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        sentences = re.split(r"(?<=[.!?؟۔])\s+", text.strip())

        sentences = [
            re.sub(r"\s+", " ", s).strip()
            for s in sentences
            if s.strip()
        ]

        chunks = []

        for i in range(0, len(sentences), self.sentences_per_chunk):
            chunk_sentences = sentences[
                i:i + self.sentences_per_chunk
            ]

            chunk = " ".join(chunk_sentences)
            chunks.append(chunk)
            
        for index, chunk in enumerate(chunks, start=1):
            print(f"\nChunk {index}:")
            print(repr(chunk))
        return chunks

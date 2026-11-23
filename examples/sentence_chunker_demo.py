
from llmforge.chunking import SentenceChunker

text = """
یادگیری ماشین یکی از شاخه‌های هوش مصنوعی است.
این حوزه به کامپیوترها کمک می‌کند از داده‌ها یاد بگیرند.
شبکه‌های عصبی یکی از روش‌های مهم در یادگیری عمیق هستند.
پردازش زبان طبیعی به کامپیوترها کمک می‌کند زبان انسان را درک کنند.
مدل‌های زبانی بزرگ می‌توانند متن تولید کنند.
"""

chunker = SentenceChunker(sentences_per_chunk=2)

print(repr(text))

chunks = chunker.chunk(text)

for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}:")
    print(chunk)

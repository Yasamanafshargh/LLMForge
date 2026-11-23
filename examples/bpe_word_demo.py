from llmforge.tokenization.bpe.bpe_trainer import BPETrainer

corpus = [
    "hello world",
    "hello there",
    "world of Python"
]

trainer = BPETrainer()

merges = trainer.train(corpus, num_merges=10)

print("\nLearned merges:")
print(merges)

print("\nFinal tokenized corpus:")
print(trainer.tokenized_corpus)
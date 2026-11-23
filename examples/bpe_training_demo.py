from llmforge.tokenization.bpe.bpe_trainer import BPETrainer


corpus = [
    "banana",
    "banana",
    "bandana"
]

trainer = BPETrainer()

merges = trainer.train(
    corpus,
    num_merges=3
)

print("\nLearned merge rules:")

for index, pair in enumerate(merges, start=1):
    print(f"{index}. {pair} -> {pair[0] + pair[1]}")


print("\nFinal corpus:")

for word in trainer.tokenized_corpus:
    print(word)
from llmforge.tokenization.bpe.bpe_trainer import BPETrainer


corpus = [
    "banana",
    "banana",
    "bandana"
]

trainer = BPETrainer()

pair_counts = trainer.count_pairs(corpus)

print("Pair frequencies:")
for pair, count in pair_counts.most_common():
    print(f"{pair}: {count}")

best_pair = pair_counts.most_common(1)[0][0]

corpus = trainer.merge_corpus(corpus, best_pair)

print("\nCorpus after merging:")
for word in corpus:
    print(word)
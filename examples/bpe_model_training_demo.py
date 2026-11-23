
from llmforge.tokenization.bpe.bpe_trainer import BPETrainer


corpus = [
    "banana",
    "banana",
    "bandana"
]

trainer = BPETrainer()

trainer.train(corpus, num_merges=3)

model = trainer.build_model(
    config={
        "algorithm": "BPE",
        "num_merges": 3,
        "initialization": "character-level",
        "pre_tokenization": "word"
    }
)

print("\nLearned merges:")
print(model.merges)

print("\nGenerated vocabulary:")
print(model.vocabulary)

print("\nSpecial tokens:")
print(model.special_tokens)

print("\nConfiguration:")
print(model.config)

model.save("data/processed/bpe_model.json")

print("\nModel saved successfully!")

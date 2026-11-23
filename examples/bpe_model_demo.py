 
from llmforge.tokenization.bpe.bpe_model import BPEModel


model = BPEModel(
    merges=[
        ("a", "n"),
        ("b", "an"),
        ("an", "a")
    ],
    vocabulary=[
        "[PAD]",
        "[UNK]",
        "[BOS]",
        "[EOS]",
        "a",
        "n",
        "an",
        "b",
        "ban",
        "ana"
    ],
    config={
        "algorithm": "BPE",
        "num_merges": 3,
        "initialization": "character-level"
    }
)

# Save model
model.save("data/processed/bpe_model.json")

print("Model saved!")

# Load model
loaded_model = BPEModel.load("data/processed/bpe_model.json")

print("\nLoaded merges:", loaded_model.merges)
print("Loaded vocabulary:", loaded_model.vocabulary)
print("Loaded config:", loaded_model.config)

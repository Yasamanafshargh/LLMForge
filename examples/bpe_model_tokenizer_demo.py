
from llmforge.tokenization.bpe.bpe_trainer import BPETrainer
from llmforge.tokenization.bpe.bpe_model import BPEModel
from llmforge.tokenization.bpe.bpe_tokenizer import BPETokenizer


# 1. Prepare training data
corpus = [
    "banana",
    "banana",
    "bandana"
]

# 2. Train BPE
trainer = BPETrainer()
trainer.train(corpus, num_merges=3)

# 3. Build the model
model = trainer.build_model(
    config={
        "algorithm": "BPE",
        "num_merges": 3,
        "pre_tokenization": "word"
    }
)

# 4. Save the model
model.save("data/processed/bpe_model.json")

# 5. Load the model
loaded_model = BPEModel.load(
    "data/processed/bpe_model.json"
)

# 6. Create tokenizer directly from the model
tokenizer = BPETokenizer.from_model(loaded_model)

# 7. Tokenize new text
text = "banana bandana!"

result = tokenizer.tokenize_with_spacing(text)

print("\nOriginal:", repr(text))
print("Tokens:", result.tokens)
print("Separators:", result.separators)
print("Reconstructed:", repr(result.reconstruct()))

print(
    "Reconstruction successful:",
    result.reconstruct() == text
)

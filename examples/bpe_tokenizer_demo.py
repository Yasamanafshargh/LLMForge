
from llmforge.tokenization.bpe.bpe_trainer import BPETrainer
from llmforge.tokenization.bpe.bpe_tokenizer import BPETokenizer


# Training data
corpus = [
    "hello world",
    "hello there",
    "world of Python"
]

# Train BPE
trainer = BPETrainer()
merges = trainer.train(corpus, num_merges=10)

# Create tokenizer using the learned rules
tokenizer = BPETokenizer(merges)

# Test on new text
text = "hello world!"

tokens = tokenizer.tokenize(text)

result = tokenizer.tokenize_with_spacing(text)

print("\nOriginal text:", repr(text))
print("Subword tokens:", tokens)
print("Separators:", result.separators)
print("Reconstructed:", repr(result.reconstruct()))

print(
    "Reconstruction successful:",
    result.reconstruct() == text
)

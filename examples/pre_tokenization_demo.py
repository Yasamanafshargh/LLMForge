
from llmforge.tokenization.pre_tokenization import WordPreTokenizer


pre_tokenizer = WordPreTokenizer()

text = "  I love   Python programming!  "

result = pre_tokenizer.pre_tokenize(text)

print("Original:", repr(text))
print("Tokens:", result.tokens)
print("Separators:", result.separators)
print("Reconstructed:", repr(result.reconstruct()))

print("Identical:", text == result.reconstruct())

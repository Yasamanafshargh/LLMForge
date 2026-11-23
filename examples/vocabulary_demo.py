from llmforge.tokenization import BasicTokenizer
from llmforge.tokenization.vocabulary import Vocabulary


tokenizer = BasicTokenizer()

text = "I love machine learning. I love AI."

tokens = tokenizer.tokenize(text)

print("Tokens:")
print(tokens)


vocabulary = Vocabulary()

vocabulary.build(tokens)

print("\nVocabulary:")
print(vocabulary.token_to_id)

print("\nVocabulary size:")
print(len(vocabulary))


encoded = vocabulary.encode(tokens)

print("\nEncoded:")
print(encoded)


decoded = vocabulary.decode(encoded)

print("\nDecoded:")
print(decoded)
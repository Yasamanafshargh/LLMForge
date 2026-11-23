from llmforge.tokenization import WhitespaceTokenizer


tokenizer = WhitespaceTokenizer()

texts = [
    "Machine learning is fascinating.",
    "یادگیری ماشین بسیار جذاب است.",
    "کتاب‌هایمان را دوست داریم.",
    "من Python را دوست دارم!"
]

for text in texts:

    tokens = tokenizer.tokenize(text)

    print("\nOriginal:", text)
    print("Tokens:", tokens)
    print("Number of tokens:", len(tokens))
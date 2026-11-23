from llmforge.tokenization import BasicTokenizer


tokenizer = BasicTokenizer()

texts = [
    "Hello, world! I love machine learning.",
    "سلام، دنیا! من هوش مصنوعی را دوست دارم.",
    "کتاب‌هایمان را دوست داریم.",
    "من Python را دوست دارم!",
    "نسخه 3.13 منتشر شد.",
    "مدل GPT-4 در سال 2025 معرفی شد."
]

for text in texts:

    tokens = tokenizer.tokenize(text)

    print("\nOriginal:", text)
    print("Tokens:", tokens)
    print("Number of tokens:", len(tokens))
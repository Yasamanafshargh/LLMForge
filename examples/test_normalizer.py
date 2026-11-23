from llmforge.cleaning.persian_normalizer import PersianNormalizer

normalizer = PersianNormalizer()

test_cases = [
    "سلام   دنیا",
    "هوش مصنوعی    و یادگیری ماشین",
    "داده‌ها دارند.   پیش‌پردازش داده‌ها",
    "  متن با فاصله اضافی  ",
]

for text in test_cases:
    result = normalizer.normalize(text)

    print(f"Before: {repr(text)}")
    print(f"After:  {repr(result)}")
    print(f"Contains double spaces: {'  ' in result}")
    print("-" * 50)
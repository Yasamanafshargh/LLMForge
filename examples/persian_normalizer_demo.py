
from llmforge.cleaning.persian_normalizer import PersianNormalizer


# Default behavior
normalizer = PersianNormalizer()

text = "  علي  در   خانه است و كتاب مي‌خواند.  "

print("Default normalization:")
print(normalizer.normalize(text))


# Digit normalization enabled
digit_normalizer = PersianNormalizer(
    normalize_digits=True
)

text_with_digits = "قیمت محصول: ١٢٥٠٠"

print("\nDigit normalization:")
print(digit_normalizer.normalize(text_with_digits))


# Disable Arabic character conversion
custom_normalizer = PersianNormalizer(
    normalize_yeh=False,
    normalize_kaf=False
)

text = "علي كتاب مي‌خواند"

print("\nCustom normalization:")
print(custom_normalizer.normalize(text))

import pytest

from llmforge.cleaning.persian_normalizer import PersianNormalizer


def test_arabic_yeh_normalization():

    normalizer = PersianNormalizer()

    result = normalizer.normalize("علي")

    assert result == "علی"


def test_arabic_kaf_normalization():

    normalizer = PersianNormalizer()

    result = normalizer.normalize("كتاب")

    assert result == "کتاب"


def test_digit_normalization():

    normalizer = PersianNormalizer(
        normalize_digits=True
    )

    result = normalizer.normalize("١٢٣٤٥٦٧٨٩٠")

    assert result == "۱۲۳۴۵۶۷۸۹۰"


def test_whitespace_normalization():

    normalizer = PersianNormalizer()

    result = normalizer.normalize("  سلام    دنیا  ")

    assert result == "سلام دنیا"


def test_half_space_preservation():

    normalizer = PersianNormalizer()

    result = normalizer.normalize("می‌روم")

    assert result == "می‌روم"


def test_custom_configuration():

    normalizer = PersianNormalizer(
        normalize_yeh=False,
        normalize_kaf=False
    )

    result = normalizer.normalize("علي كتاب")

    assert result == "علي كتاب"


def test_non_string_input():

    normalizer = PersianNormalizer()

    with pytest.raises(TypeError):
        normalizer.normalize(123)

import re
import unicodedata


class PersianNormalizer:

    def __init__(
        self,
        normalize_unicode: bool = True,
        normalize_yeh: bool = True,
        normalize_kaf: bool = True,
        normalize_digits: bool = False,
        normalize_whitespace: bool = True,
    ):
        self.normalize_unicode = normalize_unicode
        self.normalize_yeh = normalize_yeh
        self.normalize_kaf = normalize_kaf
        self.normalize_digits = normalize_digits
        self.normalize_whitespace = normalize_whitespace


    def normalize_with_steps(self, text: str) -> tuple[str, list[dict]]:
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        steps = []

        def apply_step(name, enabled, operation):
            nonlocal text

            before = text

            if enabled:
                text = operation(text)

            steps.append({
                "name": name,
                "before": before,
                "after": text,
                "status": "Applied" if enabled else "Skipped",
            })

        # 1. Unicode normalization
        apply_step(
            "Unicode Normalization (NFC)",
            self.normalize_unicode,
            lambda value: unicodedata.normalize("NFC", value),
        )

        # 2. Arabic Yeh -> Persian Yeh
        apply_step(
            "Arabic Yeh → Persian Yeh",
            self.normalize_yeh,
            lambda value: value.replace("ي", "ی"),
        )

        # 3. Arabic Kaf -> Persian Kaf
        apply_step(
            "Arabic Kaf → Persian Kaf",
            self.normalize_kaf,
            lambda value: value.replace("ك", "ک"),
        )

        # 4. Arabic-Indic digits -> Persian digits
        def convert_digits(value):
            arabic_digits = "٠١٢٣٤٥٦٧٨٩"
            persian_digits = "۰۱۲۳۴۵۶۷۸۹"

            translation_table = str.maketrans(
                arabic_digits,
                persian_digits,
            )

            return value.translate(translation_table)

        apply_step(
            "Arabic Digits → Persian Digits",
            self.normalize_digits,
            convert_digits,
        )

        # 5. Whitespace normalization
        apply_step(
            "Whitespace Normalization",
            self.normalize_whitespace,
            lambda value: re.sub(r"\s+", " ", value).strip(),
        )

        return text, steps

    def normalize(self, text: str) -> str:
        normalized_text, _ = self.normalize_with_steps(text)
        return normalized_text

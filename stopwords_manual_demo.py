from llmforge.stopwords import StopWordAnalyzer


analyzer = StopWordAnalyzer()

english_text = """
The machine learning model is learning from the data.
The model is trained with a large dataset.
"""

persian_text = """
هوش مصنوعی در حال یادگیری از داده‌ها است.
این مدل با استفاده از داده‌های بزرگ آموزش داده می‌شود.
"""

english_result = analyzer.analyze(
    english_text,
    languages=("english",),
)

persian_result = analyzer.analyze(
    persian_text,
    languages=("persian",),
)

print("ENGLISH ANALYSIS")
print("Total tokens:", english_result.total_tokens)
print("Stop words:", english_result.stop_word_count)
print("Percentage:", english_result.stop_word_percentage)
print("Frequencies:", english_result.frequencies)

print("\nPERSIAN ANALYSIS")
print("Total tokens:", persian_result.total_tokens)
print("Stop words:", persian_result.stop_word_count)
print("Percentage:", persian_result.stop_word_percentage)
print("Frequencies:", persian_result.frequencies)
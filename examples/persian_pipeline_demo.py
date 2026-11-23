
from llmforge.core.document import Document
from llmforge.core.pipeline import Pipeline
from llmforge.cleaning import PersianNormalizationStage

document = Document(
    id="1",
    text="  علي  در   خانه است و كتاب مي‌خواند.  "
)

pipeline = Pipeline([
    PersianNormalizationStage()
])

result = pipeline.run(document)

print("Original and normalized document:")
print(result.text)

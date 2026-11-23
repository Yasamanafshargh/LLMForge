
import csv
from pathlib import Path

from llmforge.core.document import Document
from llmforge.ingestion.base_loader import BaseLoader


class CSVLoader(BaseLoader):

    def __init__(self, text_field: str = "text"):
        self.text_field = text_field

    def load(self, source: str) -> list[Document]:

        file_path = Path(source)

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {source}"
            )

        if not file_path.is_file():
            raise ValueError(
                f"Source is not a file: {source}"
            )

        documents = []

        with file_path.open(
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV file has no header.")

            if self.text_field not in reader.fieldnames:
                raise ValueError(
                    f"Column '{self.text_field}' not found in CSV."
                )

            for index, row in enumerate(reader):

                text = row.get(self.text_field)

                if text is None:
                    raise ValueError(
                        f"Missing text value in row {index + 2}."
                    )

                document_id = str(row.get("id") or index)

                metadata = {
                    key: value
                    for key, value in row.items()
                    if key != self.text_field
                }

                metadata["source"] = str(file_path)
                metadata["format"] = "csv"

                documents.append(
                    Document(
                        id=document_id,
                        text=text,
                        metadata=metadata
                    )
                )

        return documents

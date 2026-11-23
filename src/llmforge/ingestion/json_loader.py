
import json
from pathlib import Path

from llmforge.core.document import Document
from llmforge.ingestion.base_loader import BaseLoader


class JSONLoader(BaseLoader):

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

        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        # Convert a single JSON object into a list
        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            raise ValueError(
                "JSON root must be an object or a list of objects."
            )

        documents = []

        for index, item in enumerate(data):

            if not isinstance(item, dict):
                raise ValueError(
                    f"Record at index {index} must be a JSON object."
                )

            if self.text_field not in item:
                raise ValueError(
                    f"Missing text field '{self.text_field}' "
                    f"in record at index {index}."
                )

            text = item[self.text_field]

            if not isinstance(text, str):
                raise ValueError(
                    f"Text field in record {index} must be a string."
                )

            document_id = str(item.get("id", index))

            metadata = {
                key: value
                for key, value in item.items()
                if key != self.text_field
            }

            metadata["source"] = str(file_path)
            metadata["format"] = "json"

            document = Document(
                id=document_id,
                text=text,
                metadata=metadata
            )

            documents.append(document)

        return documents

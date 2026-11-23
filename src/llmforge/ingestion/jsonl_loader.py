
import json
from pathlib import Path

from llmforge.core.document import Document
from llmforge.ingestion.base_loader import BaseLoader


class JSONLLoader(BaseLoader):

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

        with file_path.open("r", encoding="utf-8") as file:

            for index, line in enumerate(file):

                # Ignore empty lines
                if not line.strip():
                    continue

                try:
                    item = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(
                        f"Invalid JSON on line {index + 1}"
                    ) from error

                if not isinstance(item, dict):
                    raise ValueError(
                        f"Record on line {index + 1} must be an object."
                    )

                if self.text_field not in item:
                    raise ValueError(
                        f"Missing text field '{self.text_field}' "
                        f"on line {index + 1}."
                    )

                text = item[self.text_field]

                if not isinstance(text, str):
                    raise ValueError(
                        f"Text field on line {index + 1} "
                        "must be a string."
                    )

                document_id = str(item.get("id", index))

                metadata = {
                    key: value
                    for key, value in item.items()
                    if key != self.text_field
                }

                metadata["source"] = str(file_path)
                metadata["format"] = "jsonl"

                documents.append(
                    Document(
                        id=document_id,
                        text=text,
                        metadata=metadata
                    )
                )

        return documents

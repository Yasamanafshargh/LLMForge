from pathlib import Path

from llmforge.core.document import Document
from llmforge.ingestion.base_loader import BaseLoader


class TXTLoader(BaseLoader):

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

        text = file_path.read_text(
            encoding="utf-8"
        )

        document = Document(
            id=file_path.stem,
            text=text,
            metadata={
                "source": str(file_path),
                "format": "txt"
            }
        )

        return [document]
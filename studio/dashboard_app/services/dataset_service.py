
from pathlib import Path

from llmforge.ingestion.txt_loader import TXTLoader
from llmforge.ingestion.json_loader import JSONLoader
from llmforge.ingestion.jsonl_loader import JSONLLoader
from llmforge.ingestion.csv_loader import CSVLoader


class DatasetService:

    LOADERS = {
        "txt": TXTLoader,
        "json": JSONLoader,
        "jsonl": JSONLLoader,
        "csv": CSVLoader,
    }

    def load(self, dataset):

        if not dataset.source_file:
            raise ValueError("Dataset has no uploaded file.")

        file_path = Path(dataset.source_file.path)

        loader_class = self.LOADERS.get(dataset.file_format)

        if loader_class is None:
            raise ValueError(
                f"Unsupported dataset format: {dataset.file_format}"
            )

        loader = loader_class()

        return loader.load(str(file_path))

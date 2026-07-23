"""
bm25_index.py

Builds, saves, and loads a BM25 index for lexical retrieval.

Responsibilities:
- Build BM25 index
- Persist index to disk
- Load index from disk
- Expose indexed documents
"""

from __future__ import annotations

import pickle
from pathlib import Path

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from app.config.settings import settings
from app.exceptions.vectorstore_errors import VectorStoreError
from app.utils.logger import get_logger

logger = get_logger(__name__)


class BM25Index:
    """
    Manages the lifecycle of the BM25 index.
    """

    def __init__(self) -> None:
        self.index: BM25Okapi | None = None
        self.documents: list[Document] = []
        self.index_path: Path = settings.BM25_INDEX_DIR
        self.index_file: Path = self.index_path / "bm25.pkl"

    def build(self, documents: list[Document]) -> None:
        """
        Build a BM25 index from LangChain documents.
        """

        if not documents:
            raise VectorStoreError(
                "Cannot build BM25 index. No documents provided."
            )

        logger.info("Building BM25 index...")

        self.documents = documents

        tokenized_documents = [
            doc.page_content.split()
            for doc in documents
        ]

        self.index = BM25Okapi(tokenized_documents)

        logger.info(
            "BM25 index created with %d documents.",
            len(documents),
        )

    def save(self) -> None:
        """
        Save the BM25 index to disk.
        """

        if self.index is None:
            raise VectorStoreError(
                "BM25 index has not been built."
            )

        self.index_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(self.index_file, "wb") as file:
            pickle.dump(
                {
                    "index": self.index,
                    "documents": self.documents,
                },
                file,
            )

        logger.info(
            "BM25 index saved to %s",
            self.index_file,
        )

    def load(self) -> None:
        """
        Load BM25 index from disk.
        """

        if not self.index_file.exists():
            raise VectorStoreError(
                f"BM25 index not found: {self.index_file}"
            )

        with open(self.index_file, "rb") as file:
            data = pickle.load(file)

        self.index = data["index"]
        self.documents = data["documents"]

        logger.info(
            "BM25 index loaded successfully."
        )

    def get_index(self) -> BM25Okapi:
        """
        Return the BM25 index.
        """

        if self.index is None:
            raise VectorStoreError(
                "BM25 index is not loaded."
            )

        return self.index

    def get_documents(self) -> list[Document]:
        """
        Return indexed documents.
        """

        return self.documents
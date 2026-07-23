"""
vector_store.py

Enterprise wrapper around LangChain FAISS Vector Store.

Responsibilities:
- Create FAISS index
- Persist index
- Load index
- Execute similarity search
- Handle vector store related errors
"""

from pathlib import Path
from typing import Any

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from app.config.settings import settings
from app.exceptions.vectorstore_errors import VectorStoreError
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FAISSVectorStore:
    """
    Enterprise wrapper around LangChain FAISS Vector Store.
    """

    def __init__(self, embedding_model: Any) -> None:
        self.embedding_model = embedding_model
        self.vector_store: FAISS | None = None
        self.index_path: Path = settings.FAISS_INDEX_DIR

    def create_index(
        self,
        documents: list[Document],
    ) -> None:
        """
        Build a FAISS index from LangChain documents.
        """

        logger.info("Creating FAISS index...")

        try:

            self.vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embedding_model,
            )

            logger.info(
                "Indexed %d document(s).",
                len(documents),
            )

        except Exception as exc:

            error = VectorStoreError(
                "Failed to create FAISS index."
            )

            logger.exception("%s | Original Error: %s", error, exc)

            raise error from exc

    def save(self) -> None:
        """
        Save the FAISS index to disk.
        """

        if self.vector_store is None:
            raise VectorStoreError(
                "Vector store has not been created."
            )

        try:

            self.index_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.vector_store.save_local(
                str(self.index_path)
            )

            logger.info(
                "FAISS index saved to %s",
                self.index_path.resolve(),
            )

        except Exception as exc:

            error = VectorStoreError(
                "Failed to save FAISS index."
            )

            logger.exception("%s | Original Error: %s", error, exc)

            raise error from exc

    def load(self) -> None:
        """
        Load the persisted FAISS index.
        """

        logger.info("=" * 70)
        logger.info("Loading FAISS Index")
        logger.info("=" * 70)

        logger.info("Configured Path : %s", self.index_path)
        logger.info("Absolute Path   : %s", self.index_path.resolve())

        faiss_file = self.index_path / "index.faiss"
        pkl_file = self.index_path / "index.pkl"

        if not faiss_file.exists():
            raise VectorStoreError(
                f"FAISS index not found: {faiss_file}"
            )

        if not pkl_file.exists():
            raise VectorStoreError(
                f"Metadata file not found: {pkl_file}"
            )

        try:

            self.vector_store = FAISS.load_local(
                folder_path=str(self.index_path),
                embeddings=self.embedding_model,
                allow_dangerous_deserialization=True,
            )

            logger.info(
                "FAISS index loaded successfully."
            )

        except Exception as exc:

            error = VectorStoreError(
                "Failed to load FAISS index."
            )

            logger.exception("%s | Original Error: %s", error, exc)

            raise error from exc

    def similarity_search(
        self,
        query: str,
        k: int = 5,
    ) -> list[Document]:
        """
        Perform semantic similarity search.
        """

        if self.vector_store is None:
            raise VectorStoreError(
                "Vector store is not initialized."
            )

        return self.vector_store.similarity_search(
            query=query,
            k=k,
        )

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5,
    ) -> list:
        """
        Perform semantic similarity search and return scores.
        """

        if self.vector_store is None:
            raise VectorStoreError(
                "Vector store is not initialized."
            )

        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k,
        )

    def get_document_count(self) -> int:
        """
        Return the number of indexed vectors.
        """

        if self.vector_store is None:
            return 0

        return self.vector_store.index.ntotal
"""
chunker.py

Splits LangChain Document objects into smaller chunks while
preserving metadata for downstream retrieval.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import settings
from app.exceptions.document_errors import DocumentChunkingError
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DocumentChunker:
    """
    Splits LangChain documents into smaller overlapping chunks.
    """

    def __init__(self) -> None:
        """
        Initialize the RecursiveCharacterTextSplitter using
        project configuration.
        """

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split_documents(
        self,
        documents: list[Document],
    ) -> list[Document]:
        """
        Split documents into chunks while preserving metadata.

        Args:
            documents:
                List of LangChain Document objects.

        Returns:
            List of chunked Document objects.
        """

        if not documents:
            logger.warning("No documents received for chunking.")
            return []

        logger.info(
            "Splitting %d document(s)...",
            len(documents),
        )

        try:

            chunks = self.splitter.split_documents(documents)

            for idx, chunk in enumerate(chunks, start=1):
                chunk.metadata["chunk_id"] = idx

            logger.info(
                "Generated %d chunk(s).",
                len(chunks),
            )

            return chunks

        except Exception as exc:

            error = DocumentChunkingError(
                "Failed to split documents into chunks."
            )

            logger.exception("%s | Original Error: %s", error, exc)

            raise error from exc
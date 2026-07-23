"""
loader.py

Loads PDF documents from the configured documents directory
and converts each page into a LangChain Document object.

Responsibilities:
- Discover PDF files
- Extract text from each page
- Create LangChain Document objects
- Log ingestion progress
- Gracefully handle document loading failures
"""

from pathlib import Path

import fitz
from langchain_core.documents import Document

from app.config.settings import settings
from app.exceptions.document_errors import DocumentLoadError
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PDFLoader:
    """
    Loads PDF files and converts them into LangChain Document objects.
    """

    def __init__(self, documents_path: str | None = None) -> None:
        """
        Initialize the PDF loader.

        Args:
            documents_path:
                Optional custom documents directory.
                Defaults to the configured documents directory.
        """
        self.documents_path = Path(
            documents_path or settings.DOCS_DIR
        )


    def load_documents(self) -> list[Document]:
        """
        Load all PDF documents from the configured directory.

        Returns:
            A list of LangChain Document objects.
        """

        documents: list[Document] = []

        logger.info("Documents Path: %s", self.documents_path)
        logger.info("Absolute Path: %s", self.documents_path.resolve())

        pdf_files = list(self.documents_path.glob("*.pdf"))

        if not pdf_files:
            logger.warning(
                "No PDF files found in %s",
                self.documents_path,
            )
            return documents

        logger.info("Found %d PDF(s).", len(pdf_files))

        for pdf_file in pdf_files:

            logger.info("Loading PDF: %s", pdf_file.name)

            try:

                with fitz.open(pdf_file) as pdf:

                    for page_number, page in enumerate(pdf, start=1):

                        text = page.get_text("text").strip()

                        if not text:
                            continue

                        documents.append(
                            Document(
                                page_content=text,
                                metadata={
                                    "source": pdf_file.name,
                                    "page": page_number,
                                    "file_path": str(pdf_file),
                                },
                            )
                        )

            except Exception as exc:

                error = DocumentLoadError(
                    f"Failed to load PDF '{pdf_file.name}'."
                )

                logger.exception("%s | Original Error: %s", error, exc)

                # Continue processing remaining PDFs
                continue

        logger.info(
            "Successfully loaded %d document pages.",
            len(documents),
        )

        return documents
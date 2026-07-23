"""
build_index.py

Entry point for building document indexes.

This script executes the complete indexing pipeline, including:

1. Loading PDF documents
2. Chunking documents
3. Building the FAISS vector index
4. Building the BM25 lexical index
5. Persisting both indexes to disk
"""

from app.ingestion.pipeline import IndexingPipeline
from app.utils.logger import get_logger

logger = get_logger(__name__)


def main() -> None:
    """
    Execute the document indexing pipeline.
    """

    try:
        logger.info("Starting index build process...")

        pipeline = IndexingPipeline()
        pipeline.run()

        logger.info("Index build completed successfully.")

    except Exception as exc:
        logger.exception(
            "Index build failed: %s",
            exc,
        )
        raise


if __name__ == "__main__":
    main()
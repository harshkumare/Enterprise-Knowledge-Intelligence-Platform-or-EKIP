"""
pipeline.py

Coordinates the complete document indexing workflow.

Workflow:

PDF
    ↓
Loader
    ↓
Chunker
    ↓
Embeddings
    ↓
 ┌───────────────┐
 │               │
 ▼               ▼
FAISS          BM25
 │               │
 ▼               ▼
Save          Save
"""

from app.embeddings.embedding_model import EmbeddingModel
from app.embeddings.vector_store import FAISSVectorStore
from app.ingestion.chunker import DocumentChunker
from app.ingestion.loader import PDFLoader
from app.retrieval.bm25_index import BM25Index
from app.utils.logger import get_logger

logger = get_logger(__name__)


class IndexingPipeline:
    """
    Orchestrates the complete document indexing workflow.
    """

    def __init__(self) -> None:
        """
        Initialize all indexing components.
        """

        logger.info("Initializing Indexing Pipeline...")

        self.loader = PDFLoader()

        self.chunker = DocumentChunker()

        self.embedding_model = EmbeddingModel()

        self.vector_store = FAISSVectorStore(
            self.embedding_model.get_embeddings()
        )

        self.bm25_index = BM25Index()

    def run(self) -> None:
        """
        Execute the complete indexing workflow.
        """

        try:
            logger.info("=" * 80)
            logger.info("Starting Document Indexing Pipeline")
            logger.info("=" * 80)

            # -----------------------------------------------------
            # Load Documents
            # -----------------------------------------------------

            documents = self.loader.load_documents()

            if not documents:
                logger.warning("No documents found. Pipeline stopped.")
                return

            logger.info(
                "Loaded %d document page(s).",
                len(documents),
            )

            # -----------------------------------------------------
            # Chunk Documents
            # -----------------------------------------------------

            chunks = self.chunker.split_documents(documents)

            logger.info(
                "Created %d chunk(s).",
                len(chunks),
            )

            # -----------------------------------------------------
            # Build FAISS Index
            # -----------------------------------------------------

            logger.info("Building FAISS index...")

            self.vector_store.create_index(chunks)

            # -----------------------------------------------------
            # Build BM25 Index
            # -----------------------------------------------------

            logger.info("Building BM25 index...")

            self.bm25_index.build(chunks)

            # -----------------------------------------------------
            # Persist Indexes
            # -----------------------------------------------------

            logger.info("Saving FAISS index...")

            self.vector_store.save()

            logger.info("Saving BM25 index...")

            self.bm25_index.save()

            logger.info("=" * 80)
            logger.info("Document indexing completed successfully.")
            logger.info("=" * 80)

        except Exception as exc:
            logger.exception(
                "Indexing pipeline failed: %s",
                exc,
            )
            raise
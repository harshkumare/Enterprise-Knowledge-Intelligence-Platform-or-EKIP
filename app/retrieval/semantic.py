"""
semantic.py

Semantic retrieval layer built on top of FAISS.
"""

from typing import List

from langchain_core.documents import Document
from app.retrieval.base import BaseRetriever
from app.embeddings.embedding_model import EmbeddingModel
from app.embeddings.vector_store import FAISSVectorStore
from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SemanticRetriever(BaseRetriever):
    """
    Semantic document retriever.
    """

    def __init__(self):

        logger.info("Initializing Semantic Retriever...")

        embedding_model = EmbeddingModel()

        self.vector_store = FAISSVectorStore(
            embedding_model.get_embeddings()
        )

        self.vector_store.load()

        logger.info("Retriever initialized successfully.")

    def retrieve(
        self,
        query: str,
        k: int | None = None,
    ) -> List[Document]:
        """
        Retrieve relevant documents.
        """

        if k is None:
            k = settings.TOP_K

        logger.info(
            "Searching for: %s",
            query,
        )

        documents = self.vector_store.similarity_search(
            query=query,
            k=k,
        )

        logger.info(
            "Retrieved %d documents.",
            len(documents),
        )

        return documents
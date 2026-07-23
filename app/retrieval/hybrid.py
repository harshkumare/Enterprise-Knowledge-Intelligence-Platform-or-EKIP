"""
hybrid.py

Hybrid Retriever implementation.

Combines Semantic Search and BM25 Search
using Reciprocal Rank Fusion (RRF).
"""

from __future__ import annotations

from langchain_core.documents import Document

from app.config.settings import settings
from app.retrieval.base import BaseRetriever
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.rrf import ReciprocalRankFusion
from app.retrieval.semantic import SemanticRetriever
from app.utils.logger import get_logger

logger = get_logger(__name__)


class HybridRetriever(BaseRetriever):
    """
    Hybrid retriever combining Semantic Search
    and BM25 Search using Reciprocal Rank Fusion.
    """

    def __init__(self) -> None:
        """
        Initialize all retrievers.
        """

        self.semantic_retriever = SemanticRetriever()

        self.bm25_retriever = BM25Retriever()

        self.rrf = ReciprocalRankFusion()

    def retrieve(
        self,
        query: str,
        k: int = settings.TOP_K,
    ) -> list[Document]:
        """
        Retrieve documents using Hybrid Search.

        Args:
            query:
                User query.

            k:
                Number of final documents.

        Returns:
            Ranked list of Documents.
        """

        logger.info(
            "Running Hybrid Retrieval for query: %s",
            query,
        )

        semantic_results = self.semantic_retriever.retrieve(
            query,
            k=k,
        )

        bm25_results = self.bm25_retriever.retrieve(
            query,
            k=k,
        )

        fused_results = self.rrf.fuse(
            semantic_results,
            bm25_results,
            top_k=k,
        )

        logger.info(
            "Hybrid retrieval returned %d document(s).",
            len(fused_results),
        )

        return fused_results
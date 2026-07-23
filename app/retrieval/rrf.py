"""
rrf.py

Reciprocal Rank Fusion (RRF) implementation.

Combines multiple ranked retrieval results into a single
ranked list of unique documents.
"""

from __future__ import annotations

from collections import defaultdict

from langchain_core.documents import Document

from app.utils.logger import get_logger

logger = get_logger(__name__)


class ReciprocalRankFusion:
    """
    Implements the Reciprocal Rank Fusion (RRF) algorithm.

    Reference:
    Cormack, Clarke, and Büttcher (2009)
    """

    def __init__(self, k: int = 60) -> None:
        """
        Initialize the RRF scorer.

        Args:
            k:
                Smoothing constant.
                Standard value used in literature is 60.
        """
        self.k = k

    def fuse(
        self,
        *ranked_lists: list[Document],
        top_k: int | None = None,
    ) -> list[Document]:
        """
        Fuse multiple ranked document lists.

        Args:
            *ranked_lists:
                Ranked document lists from different retrievers.

            top_k:
                Number of final documents to return.

        Returns:
            Ranked unique documents.
        """

        logger.info(
            "Running Reciprocal Rank Fusion on %d retriever(s).",
            len(ranked_lists),
        )

        scores: dict[str, float] = defaultdict(float)
        documents: dict[str, Document] = {}

        for ranked_list in ranked_lists:

            for rank, document in enumerate(ranked_list, start=1):

                doc_id = self._document_id(document)

                documents[doc_id] = document

                scores[doc_id] += 1 / (self.k + rank)

        ranked_documents = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        results = [
            documents[doc_id]
            for doc_id, _ in ranked_documents
        ]

        if top_k is not None:
            results = results[:top_k]

        logger.info(
            "RRF returned %d document(s).",
            len(results),
        )

        return results

    @staticmethod
    def _document_id(document: Document) -> str:
        """
        Generate a stable identifier for a document.

        Uses source + page + content to uniquely identify chunks.
        """

        source = document.metadata.get("source", "")
        page = document.metadata.get("page", "")

        return f"{source}:{page}:{hash(document.page_content)}"
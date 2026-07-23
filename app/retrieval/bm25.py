"""
bm25.py

BM25 Retriever implementation.

Responsibilities:
- Load the BM25 index
- Perform lexical retrieval
- Return top-k LangChain Documents
"""

from __future__ import annotations

import numpy as np
from langchain_core.documents import Document

from app.config.settings import settings
from app.exceptions.retrieval_errors import RetrievalError
from app.retrieval.base import BaseRetriever
from app.retrieval.bm25_index import BM25Index
from app.utils.logger import get_logger

logger = get_logger(__name__)


class BM25Retriever(BaseRetriever):
    """
    BM25 lexical retriever.
    """

    def __init__(self) -> None:
        self.bm25_index = BM25Index()
        self.bm25_index.load()

    def retrieve(
        self,
        query: str,
        k: int = settings.TOP_K,
    ) -> list[Document]:
        """
        Retrieve the top-k most relevant documents.

        Args:
            query:
                User search query.

            k:
                Number of documents to return.

        Returns:
            List of LangChain Documents.
        """

        try:

            logger.info(
                "Running BM25 retrieval for query: %s",
                query,
            )

            bm25 = self.bm25_index.get_index()
            documents = self.bm25_index.get_documents()

            query_tokens = query.split()

            scores = bm25.get_scores(query_tokens)

            ranked_indices = np.argsort(scores)[::-1][:k]

            results = [
                documents[idx]
                for idx in ranked_indices
            ]

            logger.info(
                "Retrieved %d document(s).",
                len(results),
            )

            return results

        except Exception as exc:

            error = RetrievalError(
                "BM25 retrieval failed."
            )

            logger.exception(
                "%s | Original Error: %s",
                error,
                exc,
            )

            raise error from exc
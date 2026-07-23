"""
base.py

Defines the abstract interface for all retrieval implementations.

Every retriever in the project must inherit from BaseRetriever
and implement the retrieve() method.

This ensures all retrieval strategies expose a common API,
making the system extensible and compliant with SOLID principles.
"""

from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document


class BaseRetriever(ABC):
    """
    Abstract base class for all retrieval implementations.
    """

    @abstractmethod
    def retrieve(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve the top-k most relevant documents.

        Args:
            query:
                User search query.

            k:
                Number of documents to retrieve.

        Returns:
            List of LangChain Document objects.
        """
        raise NotImplementedError
"""
vectorstore_errors.py

Exceptions related to vector store operations.
"""

from app.exceptions.base import EKIPError


class VectorStoreError(EKIPError):
    """
    Raised when a vector store operation fails.
    """
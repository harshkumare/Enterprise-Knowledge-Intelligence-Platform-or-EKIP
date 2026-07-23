"""
embedding_errors.py

Exceptions related to embedding generation.
"""

from app.exceptions.base import EKIPError


class EmbeddingError(EKIPError):
    """
    Raised when embedding generation fails.
    """
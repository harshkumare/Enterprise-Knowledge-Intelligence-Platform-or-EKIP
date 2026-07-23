"""
retrieval_errors.py

Exceptions related to retrieval operations.
"""

from app.exceptions.base import EKIPError


class RetrievalError(EKIPError):
    """
    Raised when document retrieval fails.
    """
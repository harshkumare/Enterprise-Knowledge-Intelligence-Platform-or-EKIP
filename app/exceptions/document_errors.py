"""
document_errors.py

Exceptions related to document loading and processing.
"""

from app.exceptions.base import EKIPError


class DocumentLoadError(EKIPError):
    """
    Raised when a document cannot be loaded.
    """


class DocumentChunkingError(EKIPError):
    """
    Raised when document chunking fails.
    """
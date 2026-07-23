"""
Custom exception hierarchy for EKIP.
"""

from app.exceptions.base import EKIPError
from app.exceptions.document_errors import (
    DocumentChunkingError,
    DocumentLoadError,
)
from app.exceptions.embedding_errors import EmbeddingError
from app.exceptions.retrieval_errors import RetrievalError
from app.exceptions.vectorstore_errors import VectorStoreError

__all__ = [
    "EKIPError",
    "DocumentLoadError",
    "DocumentChunkingError",
    "EmbeddingError",
    "RetrievalError",
    "VectorStoreError",
]
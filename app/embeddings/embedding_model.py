"""
embedding_model.py

Loads and manages the embedding model used throughout EKIP.

Responsibilities:
- Initialize the embedding model
- Provide a reusable embedding instance
- Handle embedding initialization failures
"""

from langchain_huggingface import HuggingFaceEmbeddings

from app.config.settings import settings
from app.exceptions.embedding_errors import EmbeddingError
from app.utils.logger import get_logger

logger = get_logger(__name__)


class EmbeddingModel:
    """
    Wrapper around HuggingFace embedding models.
    """

    def __init__(self, model_name: str | None = None) -> None:
        """
        Initialize the embedding model.

        Args:
            model_name:
                Optional embedding model name.
                Defaults to the configured model.
        """

        self.model_name = model_name or settings.EMBEDDING_MODEL

        logger.info(
            "Loading embedding model: %s",
            self.model_name,
        )

        try:

            self.model = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs={
                    "device": "cpu",
                },
                encode_kwargs={
                    "normalize_embeddings": True,
                },
            )

            logger.info(
                "Embedding model loaded successfully."
            )

        except Exception as exc:

            error = EmbeddingError(
                f"Failed to initialize embedding model '{self.model_name}'."
            )

            logger.exception("%s | Original Error: %s", error, exc)

            raise error from exc

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        """
        Return the initialized embedding model.

        Returns:
            HuggingFaceEmbeddings instance.
        """

        return self.model
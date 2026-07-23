"""
settings.py
-----------

Central configuration manager for the
Enterprise Knowledge Intelligence Platform (EKIP).
"""

from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv

# ============================================================
# Project Root
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env_path = BASE_DIR / ".env"
load_dotenv(env_path)


class Settings:
    """
    Application configuration.
    """

    def __init__(self) -> None:

        # ======================================================
        # LLM Provider
        # ======================================================

        self.LLM_PROVIDER = os.getenv(
            "LLM_PROVIDER",
            "gemini",
        ).lower()

        # ======================================================
        # Groq Configuration
        # ======================================================

        self.GROQ_API_KEY = os.getenv(
            "GROQ_API_KEY"
        )

        self.GROQ_MODEL = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        )

        # ======================================================
        # Gemini Configuration
        # ======================================================

        self.GEMINI_API_KEY = os.getenv(
            "GEMINI_API_KEY"
        )

        self.GEMINI_MODEL = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

        # ======================================================
        # Hugging Face Configuration
        # ======================================================

        self.HF_TOKEN = os.getenv(
            "HF_TOKEN"
        )

        self.HF_MODEL = os.getenv(
            "HF_MODEL",
            "Qwen/Qwen3-32B",
        )

        # ======================================================
        # Generation Parameters
        # ======================================================

        self.TEMPERATURE = float(
            os.getenv("TEMPERATURE", "0.2")
        )

        self.MAX_OUTPUT_TOKENS = int(
            os.getenv("MAX_OUTPUT_TOKENS", "1024")
        )

        self.TOP_P = float(
            os.getenv("TOP_P", "0.95")
        )

        self.TOP_K_SAMPLING = int(
            os.getenv("TOP_K_SAMPLING", "40")
        )

        # ======================================================
        # Embedding Model
        # ======================================================

        self.EMBEDDING_MODEL = os.getenv(
            "EMBEDDING_MODEL",
            "BAAI/bge-small-en-v1.5",
        )

        # ======================================================
        # Project Paths
        # ======================================================

        self.BASE_DIR = BASE_DIR

        self.DOCS_DIR = BASE_DIR / "data" / "documents"
        self.DATA_DIR = BASE_DIR / "data"

        self.FAISS_INDEX_DIR = self.DATA_DIR / "faiss_index"
        self.BM25_INDEX_DIR = self.DATA_DIR / "bm25_index"

        self.LOG_DIR = BASE_DIR / "logs"
        self.TEMP_DIR = BASE_DIR / "temp"

        # ======================================================
        # Create Directories
        # ======================================================

        for directory in [
            self.DOCS_DIR,
            self.DATA_DIR,
            self.FAISS_INDEX_DIR,
            self.BM25_INDEX_DIR,
            self.LOG_DIR,
            self.TEMP_DIR,
        ]:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

        # ======================================================
        # Chunking
        # ======================================================

        self.CHUNK_SIZE = int(
            os.getenv("CHUNK_SIZE", "1000")
        )

        self.CHUNK_OVERLAP = int(
            os.getenv("CHUNK_OVERLAP", "200")
        )

        # ======================================================
        # Retrieval
        # ======================================================

        self.TOP_K = int(
            os.getenv("TOP_K", "5")
        )

        # ======================================================
        # Logging
        # ======================================================

        self.LOG_LEVEL = os.getenv(
            "LOG_LEVEL",
            "INFO",
        )


@lru_cache
def get_settings() -> Settings:
    """
    Return the singleton Settings instance.
    """
    return Settings()


settings = get_settings()
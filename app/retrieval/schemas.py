"""
schemas.py

Shared data models for retrieval and generation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from langchain_core.documents import Document


# ---------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------


@dataclass(slots=True)
class RetrievalResult:
    """
    Represents one retrieved document.
    """

    document: Document
    rank: int


# ---------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------


@dataclass(slots=True)
class Source:
    """
    Represents a document source returned with the answer.
    """

    file_name: str
    page: int
    chunk_id: str | None = None
    score: float | None = None


# ---------------------------------------------------------------------
# LLM Response
# ---------------------------------------------------------------------


@dataclass(slots=True)
class LLMResponse:
    """
    Complete response returned by the language model.
    """

    text: str

    model: str | None = None

    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

    finish_reason: str | None = None

    sources: list[Source] = field(default_factory=list)
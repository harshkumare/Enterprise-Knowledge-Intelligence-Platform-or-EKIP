"""
schemas.py

Shared data models for the generation layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Source:
    """
    Represents one retrieved source document.
    """

    file_name: str

    page: int

    chunk_id: int | None = None

    score: float | None = None


@dataclass(slots=True)
class LLMResponse:
    """
    Standard response returned by an LLM.
    """

    text: str

    model: str

    finish_reason: str | None = None

    input_tokens: int | None = None

    output_tokens: int | None = None

    total_tokens: int | None = None

    sources: list[Source] = field(default_factory=list)
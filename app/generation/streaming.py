"""
streaming.py

Streaming response schema for Enterprise RAG.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from app.generation.schemas import LLMResponse


@dataclass(slots=True)
class StreamingResponse:
    """
    Represents a streaming LLM response.

    Attributes
    ----------
    stream
        Iterator yielding response chunks.

    response
        Final populated LLMResponse after streaming
        has completed.
    """

    stream: Iterator[str]
    response: LLMResponse
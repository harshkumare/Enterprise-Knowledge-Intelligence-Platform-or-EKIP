"""
base.py

Defines the abstract interface for all Large Language Models (LLMs)
used by the Enterprise Knowledge Intelligence Platform (EKIP).

Every concrete LLM implementation (Gemini, Azure OpenAI, OpenAI,
Anthropic, etc.) must implement this interface.

This abstraction keeps the application independent from any
specific provider and follows the Dependency Inversion Principle.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator


class BaseLLM(ABC):
    """
    Abstract base class for all LLM providers.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a complete response.

        Parameters
        ----------
        prompt : str
            Fully constructed prompt.

        Returns
        -------
        str
            Complete generated response.
        """
        raise NotImplementedError

    @abstractmethod
    def stream_generate(self, prompt: str) -> Iterator[str]:
        """
        Stream a response incrementally.

        Each yielded string represents the next chunk of generated text.

        Parameters
        ----------
        prompt : str
            Fully constructed prompt.

        Yields
        ------
        str
            Next generated text chunk.
        """
        raise NotImplementedError
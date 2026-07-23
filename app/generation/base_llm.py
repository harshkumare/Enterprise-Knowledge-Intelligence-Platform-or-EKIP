from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a complete response."""
        pass

    @abstractmethod
    def stream_generate(self, prompt: str):
        """Generate a streaming response."""
        pass
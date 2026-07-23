from app.config.settings import settings
from app.generation.gemini_llm import GeminiLLM
from app.generation.groq_llm import GroqLLM


class LLMFactory:

    @staticmethod
    def create():

        provider = settings.LLM_PROVIDER.lower()

        if provider == "groq":
            return GroqLLM()

        if provider == "gemini":
            return GeminiLLM()

        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )
"""
groq_llm.py

Groq LLM implementation.
"""

from __future__ import annotations

from collections.abc import Iterator

from groq import Groq

from app.config.settings import settings
from app.exceptions.llm_errors import LLMError
from app.generation.base_llm import BaseLLM
from app.generation.schemas import LLMResponse
from app.utils.logger import get_logger


logger = get_logger(__name__)


class GroqLLM(BaseLLM):
    """
    Groq implementation of BaseLLM.
    """

    def __init__(self) -> None:
        self._client = self._create_client()
        self._model = settings.GROQ_MODEL

    @property
    def model_name(self) -> str:
        return self._model

    def _create_client(self) -> Groq:

        logger.info("Initializing Groq client.")

        try:
            return Groq(
                api_key=settings.GROQ_API_KEY,
            )

        except Exception as exc:
            logger.exception(
                "Failed to initialize Groq client."
            )

            raise LLMError(
                "Unable to initialize Groq client."
            ) from exc

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        logger.info("Sending prompt to Groq.")

        try:

            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_OUTPUT_TOKENS,
                top_p=settings.TOP_P,
                stream=False,
            )

            text = response.choices[0].message.content or ""

            usage = response.usage

            return LLMResponse(
                text=text,
                model=self._model,
                finish_reason=response.choices[0].finish_reason,
                input_tokens=usage.prompt_tokens if usage else None,
                output_tokens=usage.completion_tokens if usage else None,
                total_tokens=usage.total_tokens if usage else None,
            )

        except Exception as exc:

            logger.exception(
                "Groq generation failed."
            )

            raise LLMError(
                "Failed to generate response from Groq."
            ) from exc

    def stream_generate(
        self,
        prompt: str,
    ) -> Iterator[str]:

        logger.info("Streaming response from Groq.")

        try:

            stream = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_OUTPUT_TOKENS,
                top_p=settings.TOP_P,
                stream=True,
            )

            for chunk in stream:

                if (
                    chunk.choices
                    and chunk.choices[0].delta.content
                ):
                    yield chunk.choices[0].delta.content

            logger.info(
                "Groq streaming completed."
            )

        except Exception as exc:

            logger.exception(
                "Groq streaming failed."
            )

            raise LLMError(
                "Failed to stream response from Groq."
            ) from exc
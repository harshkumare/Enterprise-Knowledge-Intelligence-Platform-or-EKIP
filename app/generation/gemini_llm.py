"""
gemini_llm.py

Gemini LLM implementation.
"""

from __future__ import annotations

from collections.abc import Iterator

from google import genai
from google.genai import types

from app.config.settings import settings
from app.exceptions.llm_errors import LLMError
from app.generation.base_llm import BaseLLM
from app.generation.schemas import LLMResponse
from app.utils.logger import get_logger


logger = get_logger(__name__)


class GeminiLLM(BaseLLM):
    """
    Gemini implementation of BaseLLM.
    """

    def __init__(self) -> None:
        self._client = self._create_client()
        self._model = settings.GEMINI_MODEL

    @property
    def model_name(self) -> str:
        """
        Return the configured Gemini model name.
        """
        return self._model

    def _create_client(self) -> genai.Client:
        """
        Create and return a Gemini client.
        """

        logger.info("Initializing Gemini client.")

        try:
            return genai.Client(
                api_key=settings.GEMINI_API_KEY,
            )

        except Exception as exc:
            logger.exception(
                "Failed to initialize Gemini client."
            )

            raise LLMError(
                "Unable to initialize Gemini client."
            ) from exc

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:
        """
        Generate a complete response from Gemini.
        """

        logger.info("Sending prompt to Gemini.")

        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.TEMPERATURE,
                    top_p=settings.TOP_P,
                    top_k=settings.TOP_K_SAMPLING,
                    max_output_tokens=settings.MAX_OUTPUT_TOKENS,
                ),
            )

            logger.info("Gemini response received.")

            input_tokens = self._extract_input_tokens(response)
            output_tokens = self._extract_output_tokens(response)

            return LLMResponse(
                text=response.text or "",
                model=self._model,
                finish_reason=self._extract_finish_reason(response),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=(
                    input_tokens + output_tokens
                    if input_tokens is not None
                    and output_tokens is not None
                    else None
                ),
            )

        except Exception as exc:
            logger.exception(
                "Gemini generation failed."
            )

            raise LLMError(
                "Failed to generate response from Gemini."
            ) from exc

    def stream_generate(
        self,
        prompt: str,
    ) -> Iterator[str]:
        """
        Stream a response from Gemini.

        Yields
        ------
        str
            Incremental text chunks produced by Gemini.
        """

        logger.info("Streaming response from Gemini.")

        try:
            stream = self._client.models.generate_content_stream(
                model=self._model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.TEMPERATURE,
                    top_p=settings.TOP_P,
                    top_k=settings.TOP_K_SAMPLING,
                    max_output_tokens=settings.MAX_OUTPUT_TOKENS,
                ),
            )

            for chunk in stream:
                text = getattr(chunk, "text", None)

                if text:
                    yield text

            logger.info("Gemini streaming completed.")

        except Exception as exc:
            logger.exception(
                "Gemini streaming failed."
            )

            raise LLMError(
                "Failed to stream response from Gemini."
            ) from exc

    @staticmethod
    def _extract_finish_reason(
        response,
    ) -> str | None:
        """
        Extract finish reason safely.
        """

        try:
            candidate = response.candidates[0]
            reason = candidate.finish_reason

            return str(reason) if reason else None

        except Exception:
            return None

    @staticmethod
    def _extract_input_tokens(
        response,
    ) -> int | None:
        """
        Extract prompt token count.
        """

        try:
            return response.usage_metadata.prompt_token_count

        except Exception:
            return None

    @staticmethod
    def _extract_output_tokens(
        response,
    ) -> int | None:
        """
        Extract generated token count.
        """

        try:
            return response.usage_metadata.candidates_token_count

        except Exception:
            return None
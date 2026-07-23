"""
response_generator.py

Coordinates the complete Retrieval-Augmented
Generation (RAG) pipeline.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from app.generation.context_builder import ContextBuilder
from app.generation.base_llm import BaseLLM
from app.generation.llm_factory import LLMFactory
from app.generation.memory import ConversationMemory
from app.generation.prompts import PromptBuilder
from app.generation.schemas import (
    LLMResponse,
    Source,
)
from app.retrieval.base import BaseRetriever


class ResponseGenerator:
    """
    Coordinates the complete RAG pipeline.
    """

    def __init__(
        self,
        retriever: BaseRetriever,
        llm: BaseLLM | None = None,
    ) -> None:
        self._retriever = retriever

        # Create provider automatically if none is supplied
        self._llm = llm or LLMFactory.create()

        self._memory = ConversationMemory()

        # Stores the latest completed response
        self.last_response: LLMResponse | None = None

    def generate(
        self,
        question: str,
    ) -> LLMResponse:
        """
        Generate a complete answer.
        """

        prompt, documents = self._prepare_generation(question)

        response = self._llm.generate(prompt)

        self._attach_sources(
            response=response,
            documents=documents,
        )

        self.last_response = response

        self._update_memory(
            question=question,
            answer=response.text,
        )

        return response

    def stream_generate(
        self,
        question: str,
    ) -> Iterator[str]:
        """
        Stream an answer while storing the final response.
        """

        prompt, documents = self._prepare_generation(question)

        full_response = ""

        for chunk in self._llm.stream_generate(prompt):
            full_response += chunk
            yield chunk

        response = LLMResponse(
            text=full_response,
            model=self._llm.model_name,
        )

        self._attach_sources(
            response=response,
            documents=documents,
        )

        self.last_response = response

        self._update_memory(
            question=question,
            answer=full_response,
        )

    def _prepare_generation(
        self,
        question: str,
    ) -> tuple[str, list[Any]]:
        """
        Execute retrieval and build prompt.
        """

        documents = self._retriever.retrieve(question)

        context = ContextBuilder.build(documents)

        history = self._memory.format_history()

        prompt = PromptBuilder.build_rag_prompt(
            question=question,
            context=context,
            history=history,
        )

        return prompt, documents

    @staticmethod
    def _attach_sources(
        response: LLMResponse,
        documents: list[Any],
    ) -> None:
        """
        Attach unique sources to the response.
        """

        seen: set[tuple[str, int]] = set()
        sources: list[Source] = []

        for document in documents:

            file_name = document.metadata.get(
                "source",
                "Unknown",
            )

            page = document.metadata.get(
                "page",
                0,
            )

            score = document.metadata.get(
                "score",
            )

            chunk_id = document.metadata.get(
                "chunk_id",
            )

            key = (file_name, page)

            if key in seen:
                continue

            seen.add(key)

            sources.append(
                Source(
                    file_name=file_name,
                    page=page,
                    chunk_id=chunk_id,
                    score=score,
                )
            )

        response.sources = sources

    def _update_memory(
        self,
        question: str,
        answer: str,
    ) -> None:
        """
        Store conversation in memory.
        """

        self._memory.add_user_message(question)
        self._memory.add_assistant_message(answer)

    def clear_memory(self) -> None:
        """
        Clear conversation history.
        """

        self._memory.clear()
        self.last_response = None
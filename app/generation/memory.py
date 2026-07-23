"""
memory.py

Conversation memory implementation for EKIP.

Stores recent chat history and formats it for prompt generation.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(slots=True)
class Message:
    """
    Represents a single chat message.
    """

    role: str
    content: str


class ConversationMemory:
    """
    Stores recent conversation history.
    """

    def __init__(
        self,
        max_messages: int = 10,
    ) -> None:
        self._messages: deque[Message] = deque(
            maxlen=max_messages
        )

    def add_user_message(
        self,
        message: str,
    ) -> None:
        """
        Store a user message.
        """
        self._messages.append(
            Message(
                role="User",
                content=message,
            )
        )

    def add_assistant_message(
        self,
        message: str,
    ) -> None:
        """
        Store an assistant message.
        """
        self._messages.append(
            Message(
                role="Assistant",
                content=message,
            )
        )

    def clear(self) -> None:
        """
        Clear conversation history.
        """
        self._messages.clear()

    def get_messages(
        self,
    ) -> list[Message]:
        """
        Return all stored messages.
        """
        return list(self._messages)

    def format_history(
        self,
    ) -> str:
        """
        Convert history into a prompt-friendly format.
        """

        if not self._messages:
            return ""

        history = []

        for message in self._messages:
            history.append(
                f"{message.role}: {message.content}"
            )

        return "\n".join(history)
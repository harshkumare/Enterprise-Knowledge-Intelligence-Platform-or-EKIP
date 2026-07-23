"""
context_builder.py

Builds the context supplied to the LLM.
"""

from __future__ import annotations

from langchain_core.documents import Document


class ContextBuilder:
    """
    Builds formatted context from retrieved documents.
    """

    @staticmethod
    def build(
        documents: list[Document],
    ) -> str:
        """
        Convert retrieved documents into a formatted context string.

        Args:
            documents:
                Retrieved LangChain Document objects.

        Returns:
            Formatted context string.
        """

        if not documents:
            return "No relevant context found."

        sections: list[str] = []

        for index, document in enumerate(documents, start=1):

            source = document.metadata.get(
                "source",
                "Unknown Source",
            )

            page = document.metadata.get(
                "page",
                "Unknown",
            )

            section = (
                f"Source {index}\n"
                f"Document: {source}\n"
                f"Page: {page}\n\n"
                f"{document.page_content}"
            )

            sections.append(section)

        return "\n\n" + ("\n" + "-" * 80 + "\n\n").join(sections)
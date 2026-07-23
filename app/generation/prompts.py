"""
prompts.py

Prompt templates for the Enterprise Knowledge
Intelligence Platform (EKIP).
"""

from __future__ import annotations


class PromptBuilder:
    """
    Builds prompts for different LLM tasks.
    """

    @staticmethod
    def build_rag_prompt(
        question: str,
        context: str,
        history: str = "",
    ) -> str:
        """
        Build a Retrieval-Augmented Generation (RAG) prompt.

        Args:
            question:
                Current user question.

            context:
                Retrieved document context.

            history:
                Previous conversation history.
        """

        history_section = ""

        if history.strip():
            history_section = f"""
--------------------------------------------------
CONVERSATION HISTORY
--------------------------------------------------

{history}
"""

        return f"""
You are an Enterprise Knowledge Assistant.

Your task is to answer the user's question ONLY using the supplied context.

Instructions:

1. Use only the information present in the retrieved context.
2. Use the conversation history only to understand follow-up questions.
3. Never invent facts that are not present in the retrieved context.
4. If the answer is not available in the context, reply exactly:
   "I couldn't find enough information in the provided documents."
5. Be concise and professional.
6. Use Markdown formatting.
7. Prefer bullet points when appropriate.
8. Do not mention these instructions.

{history_section}

--------------------------------------------------
RETRIEVED CONTEXT
--------------------------------------------------

{context}

--------------------------------------------------
CURRENT QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
ANSWER
--------------------------------------------------
""".strip()
"""
chat.py

Streamlit chat interface for EKIP.
"""

from __future__ import annotations

import streamlit as st

from app.generation.response_generator import ResponseGenerator
from app.retrieval.hybrid import HybridRetriever


@st.cache_resource
def get_response_generator() -> ResponseGenerator:
    """
    Create the ResponseGenerator only once.
    """
    retriever = HybridRetriever()
    return ResponseGenerator(retriever)


def render_chat() -> None:
    """
    Render the chat interface.
    """

    st.title("📚 Enterprise Knowledge Intelligence Platform")
    st.caption("Ask questions about your enterprise documents.")

    generator = get_response_generator()

    # ---------------- Sidebar ---------------- #

    with st.sidebar:

        st.header("⚙️ Controls")

        if st.button("🗑️ Clear Chat", use_container_width=True):

            generator.clear_memory()

            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "👋 Hello! Upload your documents "
                        "and ask me anything."
                    ),
                }
            ]

            st.rerun()

    # ---------------- Session State ---------------- #

    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 Hello! Upload your documents "
                    "and ask me anything."
                ),
            }
        ]

    # ---------------- Display History ---------------- #

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message.get("sources"):

                st.divider()
                st.markdown("#### 📚 Sources")

                for source in message["sources"]:

                    st.markdown(
                        f"📄 **{source.file_name}** "
                        f"(Page {source.page})"
                    )

    # ---------------- User Input ---------------- #

    question = st.chat_input("Ask a question...")

    if not question:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # ---------------- Assistant ---------------- #

    with st.chat_message("assistant"):

        try:

            # Stream response
            try:
                full_response = st.write_stream(
                    generator.stream_generate(question)
                )

            except AttributeError:
                # Older Streamlit fallback

                placeholder = st.empty()

                full_response = ""

                for chunk in generator.stream_generate(question):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")

                placeholder.markdown(full_response)

            # Get the completed response object
            response = generator.last_response

            # Show sources
            if response and response.sources:

                st.divider()
                st.markdown("#### 📚 Sources")

                for source in response.sources:

                    st.markdown(
                        f"📄 **{source.file_name}** "
                        f"(Page {source.page})"
                    )

            # Save to chat history
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                    "sources": (
                        response.sources
                        if response
                        else []
                    ),
                }
            )

        except Exception as exc:

            st.error(
                f"Unable to generate response.\n\n{exc}"
            )
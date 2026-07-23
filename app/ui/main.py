"""
main.py

Streamlit entry point for the Enterprise Knowledge
Intelligence Platform (EKIP).
"""

from __future__ import annotations

import streamlit as st

from app.ui.chat import render_chat
from app.ui.uploader import render_uploader


def configure_page() -> None:
    """
    Configure the Streamlit application.
    """

    st.set_page_config(
        page_title="Enterprise Knowledge Intelligence Platform",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_sidebar() -> None:
    """
    Render the application sidebar.
    """

    with st.sidebar:

        st.title("📚 EKIP")

        st.markdown("---")

        render_uploader()

        st.markdown("---")

        st.header("About")

        st.markdown(
            """
            **Enterprise Knowledge Intelligence Platform**

            Enterprise RAG chatbot powered by:

            - 🤖 Google Gemini
            - 🔗 LangChain
            - 📚 FAISS
            - 🔍 BM25
            - ⚡ Hybrid Retrieval
            - 🎈 Streamlit
            """
        )


def main() -> None:
    """
    Application entry point.
    """

    configure_page()

    render_sidebar()

    render_chat()


if __name__ == "__main__":
    main()
"""
uploader.py

Handles PDF upload and document indexing.
"""

from __future__ import annotations

import streamlit as st

from app.config.settings import settings
from app.ingestion.pipeline import IndexingPipeline

DOCUMENTS_DIR = settings.DOCS_DIR


def render_uploader() -> None:
    """
    Render the PDF uploader.
    """

    st.header("📄 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF file(s)",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        return

    if st.button("📥 Upload & Index Documents"):

        DOCUMENTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        with st.spinner("Uploading and indexing documents..."):

            try:

                for uploaded_file in uploaded_files:

                    destination = DOCUMENTS_DIR / uploaded_file.name

                    with open(destination, "wb") as file:
                        file.write(uploaded_file.getbuffer())

                pipeline = IndexingPipeline()
                pipeline.run()

                # Clear cached retriever
                st.cache_resource.clear()

                st.success("✅ Documents indexed successfully!")

                st.rerun()

            except Exception as exc:

                st.error(f"Indexing failed:\n{exc}")
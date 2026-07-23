"""
query_index.py

Interactive CLI for querying document indexes.

Supports:
1. Semantic Search (FAISS)
2. BM25 Search
3. Hybrid Search (RRF)
"""

from app.retrieval.bm25 import BM25Retriever
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.semantic import SemanticRetriever
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_retriever():
    """
    Allow the user to choose a retrieval strategy.
    """

    while True:

        print("\nChoose Retrieval Method")
        print("1. Semantic Search (FAISS)")
        print("2. BM25 Search")
        print("3. Hybrid Search (RRF)")

        choice = input("\nEnter choice (1/2/3): ").strip()

        if choice == "1":
            logger.info("Using Semantic Retriever.")
            return SemanticRetriever()

        if choice == "2":
            logger.info("Using BM25 Retriever.")
            return BM25Retriever()

        if choice == "3":
            logger.info("Using Hybrid Retriever.")
            return HybridRetriever()

        print("\n❌ Invalid choice. Please try again.")


def display_results(docs) -> None:
    """
    Display retrieved documents.
    """

    print("\n" + "=" * 80)

    if not docs:
        print("\nNo documents retrieved.")
        print("=" * 80)
        return

    for i, doc in enumerate(docs, start=1):

        print(f"\nResult {i}")
        print("-" * 80)

        print(doc.page_content[:600])

        print()

        print(doc.metadata)

    print("=" * 80)


def main() -> None:
    """
    Start the interactive retrieval CLI.
    """

    try:

        retriever = get_retriever()

        while True:

            print()

            query = input(
                "Ask a question (type 'exit' to quit): "
            ).strip()

            if query.lower() == "exit":
                logger.info("Exiting query application.")
                break

            docs = retriever.retrieve(query)

            display_results(docs)

    except Exception as exc:

        logger.exception(
            "Query application failed: %s",
            exc,
        )
        raise


if __name__ == "__main__":
    main()
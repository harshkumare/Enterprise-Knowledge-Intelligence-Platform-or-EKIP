from app.embeddings.embedding_model import EmbeddingModel
from app.embeddings.vector_store import FAISSVectorStore
from app.retrieval.semantic import SemanticRetriever
from app.generation.response_generator import ResponseGenerator


def main() -> None:
    print("=" * 60)
    print("Enterprise Knowledge Intelligence Platform")
    print("Type 'exit' to quit.")
    print("=" * 60)

    # Initialize embedding model

    # Create retriever
    retriever = SemanticRetriever()
    # Create response generator
    generator = ResponseGenerator(retriever)

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        response = generator.generate(question)

        print("\nAssistant:\n")
        print(response.text)


if __name__ == "__main__":
    main()
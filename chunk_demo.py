from app.ingestion.loader import PDFLoader
from app.ingestion.chunker import DocumentChunker

loader = PDFLoader()
documents = loader.load_documents()

print(f"Documents Loaded: {len(documents)}")

chunker = DocumentChunker()
chunks = chunker.split_documents(documents)

print(f"Chunks Created: {len(chunks)}")

if len(chunks) > 0:
    print("\nFirst Chunk Metadata")
    print(chunks[0].metadata)

    print("\nPreview\n")
    print(chunks[0].page_content[:500])
else:
    print("❌ No chunks were created.")
from app.config.settings import get_settings

settings = get_settings()

print("Gemini Key Exists :", bool(settings.GOOGLE_API_KEY))
print("Embedding Model   :", settings.EMBEDDING_MODEL)
print("Chunk Size        :", settings.CHUNK_SIZE)
print("Chunk Overlap     :", settings.CHUNK_OVERLAP)
print("Top K             :", settings.TOP_K)

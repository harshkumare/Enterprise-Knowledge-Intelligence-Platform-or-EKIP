from app.embeddings.embedding_model import EmbeddingModel

embedding_model = EmbeddingModel()

model = embedding_model.get_model()

vector = model.embed_query("What is Retrieval Augmented Generation?")

print(f"Embedding Dimension: {len(vector)}")

print(vector[:10])

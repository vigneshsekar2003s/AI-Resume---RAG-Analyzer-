from sentence_transformers import SentenceTransformer

# Load the embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    """
    Convert resume chunks into numerical vectors.
    """

    if not chunks:
        return []

    embeddings = embedding_model.encode(
        chunks,
        normalize_embeddings=True
    )

    return embeddings
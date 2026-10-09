import faiss


def create_faiss_index(embeddings):
    """
    Create a FAISS index using normalized embeddings.
    """

    if embeddings is None or len(embeddings) == 0:
        return None

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


def search_faiss(index, query_embedding, top_k=4):
    """
    Search the FAISS index and return the most relevant chunk indexes
    and similarity scores.
    """

    if index is None:
        return [], []

    scores, indices = index.search(query_embedding, top_k)

    return indices[0], scores[0]
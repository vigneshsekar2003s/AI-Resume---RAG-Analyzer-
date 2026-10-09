def create_chunks(text, chunk_size=700, overlap=100):
    """
    Split resume text into overlapping chunks.

    chunk_size:
        Maximum approximate number of characters per chunk.

    overlap:
        Number of characters repeated between consecutive chunks.
    """

    if not text:
        return []

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - overlap

    return chunks
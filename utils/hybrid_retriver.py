from rank_bm25 import BM25Okapi


def hybrid_retrieve(
    vector_store,
    chunks,
    query,
    k=3
):
    # BM25 Search
    tokenized_chunks = [
        doc.page_content.split()
        for doc in chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    scores = bm25.get_scores(
        query.split()
    )

    bm25_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:k]

    bm25_docs = [
        chunks[i]
        for i in bm25_indices
    ]

    # Vector Search
    vector_docs = vector_store.similarity_search(
        query,
        k=k
    )

    # Merge Results
    merged = []
    seen = set()

    for doc in bm25_docs + vector_docs:

        content = doc.page_content

        if content not in seen:
            merged.append(doc)
            seen.add(content)

    return merged[:k]
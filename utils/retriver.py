def retrieve_documents(
    vector_store,
    query,
    k=3
):
    retriever = vector_store.as_retriever(
        search_kwargs={"k": k}
    )

    docs = retriever.invoke(query)

    return docs
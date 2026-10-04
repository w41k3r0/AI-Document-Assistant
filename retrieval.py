def retrieve_chunks(vector_store, question, top_k=4):
    question = question.strip()
    if not question:
        raise ValueError("Please enter a question.")

    retriever = vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k" : top_k}
    )

    relevant_chunks = retriever.invoke(question)

    return relevant_chunks

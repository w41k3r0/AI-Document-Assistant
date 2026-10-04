from langchain_community.vectorstores import FAISS
from embeddings import embed_chunks, get_embedding_model

def create_vector_store(chunks):
    if not chunks:
        raise ValueError("No text chunks were available to index.")

    vectors = embed_chunks(chunks)

    text_vector_pairs = []
    metadata = []
    
    for chunk, vector in zip(chunks, vectors):
        text_vector_pairs.append(
            chunk.page_content, vector
        )
        metadata.append(chunk.metadata)

    vector_store = FAISS.from_embeddings(
        text_embeddings = text_vector_pairs,
        embedding = get_embedding_model(),
        metadatas = metadata,
    )

    return vector_store

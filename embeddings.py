from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings

@lru_cache(maxsize=1)
def get_embedding_model():
    model = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs = {"device" : "cpu"},
        encoding_kwargs = {"normalize_embeddings" : True},
    )

    return model

def embed_chunks(chunks):
    model = get_embedding_model()

    texts = []

    for chunk in chunks:
        texts.append(chunk.page_content)

    vectors = model.embed_documents(texts)

    return vectors

from pathlib import Path
from uuid import uuid4
from vector_store import create_vector_store
from chunking import create_chunks

def process_documents(pdf_paths):
    all_chunks = []
    documents = []

    for pdf_path in pdf_paths:
        pdf_path = Path(pdf_path)
        document_id = uuid4().hex

        chunks = create_chunks(pdf_path)

        if not chunks:
            raise RuntimeError(f"No readable text was found in {pdf_path.name}.")


        for number, chunk in enumerate(chunks, start=1):
            chunk.metadata["document_id"] = document_id
            chunk.metadata["chunk_id"] = (
                f"{document_id}-chunk-{number}"
            )

        all_chunks.extend(chunks)

        documents.append({
            "document_id" : document_id,
            "source" : pdf_path.name,
            "chunk_count" : len(chunks),
        })

    if not all_chunks:
        raise ValueError("Please provide atleast one readable PDF.")

    vector_store = create_vector_store(all_chunks)

    return {
        "vector_store" : vector_store,
        "documents" : documents,
    }

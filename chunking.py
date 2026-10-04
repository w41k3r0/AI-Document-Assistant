from transformers import AutoTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from prepare_documents import prepare_documents

def create_chunks(pdf_path):
    documents = prepare_documents(pdf_path)

    tokenizer = AutoTokenizer.from_pretrained(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer,
        chunk_size = 220,
        chunk_overlap = 40,
    )

    chunks = splitter.split_documents(documents)

    return chunks

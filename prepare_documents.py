from langchain_core.documents import Document
from prepare_pages import prepare_pages

def prepare_documents(pdf_path):
    pages = prepare_pages(pdf_path)

    documents = []

    for page in pages:
        document = Document(
            page_content = page["text"],
            metadata = {
                "page" : page["page"],
                "source" : page["source"],
            }
        )
        documents.append(document)

    return documents

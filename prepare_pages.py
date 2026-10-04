from extract_pdf import extract_pdf
from cleaning import clean_text

def prepare_pages(pdf_path):
    pages = extract_pdf(pdf_path)

    for page in pages:
        page["text"] = clean_text(page["text"])

    return pages

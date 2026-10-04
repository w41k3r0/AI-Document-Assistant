from pathlib import Path
import pymupdf

def extract_pdf(pdf_path):
    pdf_path = Path(pdf_path)
    pages = []
    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            pages.append({
                "page" : page_number,
                "text" : page.get_text(),
                "source" : pdf_path.name
            })
    
    return pages

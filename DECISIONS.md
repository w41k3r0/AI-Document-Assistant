# Design Decisions

## 1. Flask for the Backend

Flask was selected because the project requires custom routes for file uploads, question requests, session handling, and error responses. It also keeps the backend structure understandable for an interview demonstration.

## 2. Tailwind CSS for the Interface

Tailwind CSS was selected to create a responsive dark interface directly in the HTML template. Its utility classes make it easy to adjust spacing, typography, borders, and responsive breakpoints.

## 3. PDF-Only Scope

The first version supports PDF files only. Restricting the input format keeps extraction and validation predictable and matches the intended interview demonstration.

## 4. PyMuPDF for Text Extraction

PyMuPDF extracts text page by page and provides page numbers. Keeping page metadata makes it possible to display useful source locations with generated answers.

## 5. Token-Based Chunking

The project uses the Hugging Face tokenizer for `all-MiniLM-L6-v2` and `RecursiveCharacterTextSplitter`. Token-based chunking keeps passages within a predictable size for embedding and retrieval.

## 6. Local Embeddings

The project uses `sentence-transformers/all-MiniLM-L6-v2` locally instead of an embedding API. This avoids a second paid or quota-limited API dependency.

The trade-off is that the embedding model consumes local memory and CPU time, especially during the first upload.

## 7. FAISS for Vector Search

FAISS was selected because it provides fast similarity search and works well for a small interview-scale document collection.

The vector store is kept in memory because persistent storage is outside the scope of this MVP.

## 8. Gemini for Answer Generation

Google Gemini was selected for answer generation because it can be accessed through an API key and integrates with LangChain.

The model receives the user’s question and retrieved passages. It is instructed to answer only from those passages and cite their labels.

## 9. Citation Validation

The model must cite passages using labels such as `[S1]` and `[S2]`. The backend checks the labels and returns only the source passages that were actually cited.

This makes the displayed citations traceable to retrieved document chunks.

## 10. In-Memory Session Collections

Each browser session receives a session identifier. The server stores that session’s vector store in an in-memory dictionary.

This is simple and suitable for a small demonstration, but it is not persistent across server restarts and is not suitable for a multi-instance production deployment.

## 11. Browser Fetch Requests

The frontend uses `fetch()` so uploads and questions can be processed without reloading the page.

Files are sent with `FormData`, while questions are sent as JSON.

## 12. Markdown Rendering

Assistant responses are converted from Markdown to HTML using Marked. DOMPurify sanitizes the generated HTML before it is inserted into the page.

User questions, filenames, and source passages continue to use `textContent`.

## 13. One Render Worker

Render is configured with one Gunicorn worker because the current in-memory collection dictionary is not shared between separate worker processes.

A persistent database or external vector store would be required before scaling to multiple workers or instances.
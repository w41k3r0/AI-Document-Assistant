**AI Document Assistant**

This is a Flask project that lets users upload PDF files and ask questions about them. It extracts the text from the PDFs, searches for relevant parts, and uses Google Gemini to generate an answer.

## Features
- Upload up to 5 PDF files.
- Total upload request limit: 20 MiB.
- Ask questions about one or more uploaded PDFs.
- Show the source file and page used for an answer.
- Use a dark, responsive interface made with Tailwind CSS.
- Upload files and ask questions without refreshing the page.

## Technologies used
- Python and Flask
- PyMuPDF for reading PDF text
- Sentence Transformers (all-MiniLM-L6-v2) for local embeddings
- FAISS for similarity search
- Google Gemini for generating answers
- Tailwind CSS and JavaScript for the interface

## How the project works
- The user uploads PDF files.
- Text is extracted from each page.
- The text is split into smaller chunks.
- The chunks are converted into embeddings.
- FAISS finds the chunks most related to the question.
- The relevant chunks are sent to Gemini.
- The answer and its sources are shown on the page.

## Limitations
- The Render deployment was not performance-tested before submission, so its exact memory usage and startup time are unknown.
- The expected use is one or two users uploading one or two short PDFs during the interview.
- Render's free service may sleep after inactivity.
- Uploaded files and the FAISS index are kept in memory and are lost when the app restarts.
- Users may need to upload their PDFs again after a restart.
- The app does not save conversation history.
- Scanned or image-only PDFs may not work correctly because OCR is not included.
- The app does not currently have user accounts or rate limiting.

## Run locally
- Clone or download this repository and open a terminal in the project folder.
- Create and activate a virtual environment:
   For Windows: 
                python -m venv .venv
                .venv\Scripts\activate
   For macOS/Linux:
                python3 -m venv .venv
                source .venv/bin/activate
- Install the required libraries:
    pip install -r requirements.txt
- Create a .env file in the project folder, beside app.py:
    GOOGLE_API_KEY=your-gemini-api-key
    GEMINI_MODEL=gemini-3.8-flash
    SESSION_KEY=your-random-session-key
    A session key can be generated with:
    python -c "import secrets; print(secrets.token_hex(32))"
- Start the Flask app:
    python app.py
- Open the local address shown in the terminal, usually http://127.0.0.1:5000.
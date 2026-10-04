import os
from flask import Flask, jsonify, request, session, render_template
from ingestion import process_documents
from dotenv import load_dotenv
from uuid import uuid4
from pathlib import Path
from tempfile import TemporaryDirectory
from werkzeug.utils import secure_filename
from rag import answer_question

load_dotenv(Path(__file__).parent / ".env")

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SESSION_KEY")
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

if not app.config["SECRET_KEY"]:
    raise ValueError("SESSION_KEY is missing!")

collections = {}

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/upload")
def upload_documents():
    files = request.files.getlist("files")
    if not files:
        return jsonify({
            "error" : "Please select PDF files."
        }), 400

    if len(files) > 5:
        return jsonify({
            "error" : "Upload limit of 5 PDFs has been reached."
        }), 400

    file_names = []

    for file in files:
        file_name = secure_filename(file.filename or "")

        if not file_name or not file_name.lower().endswith(".pdf"):
            return jsonify({
                "error" : "Files must be a PDF."
            }), 400

        file_names.append(file_name)

    if "session_id" not in session:
        session["session_id"] = uuid4().hex

    try:
        with TemporaryDirectory() as temp_folder:
            pdf_paths = []

            for file, file_name in zip(files, file_names):
                file_folder = Path(temp_folder) / uuid4().hex
                file_folder.mkdir()

                pdf_path = file_folder / file_name
                file.save(pdf_path)
                pdf_paths.append(pdf_path)

            collection = process_documents(pdf_paths)

    except Exception:
        app.logger.exception("Document processing failed.")

        return jsonify({
            "error" : (
                "The documents could not be processed. "
                "Make sure that they are readable, unencrypted PDFs "
                "and try again."
            )
        }), 422

    collections[session["session_id"]] = collection

    return jsonify({
        "message" : "Documents are ready.",
        "documents" : collection["documents"],
    })

@app.post("/api/ask")
def ask_question():
    if not request.is_json:
        return jsonify({
            "error" : "The request must contain JSON."
        }), 415

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error" : "Please send a valid JSON object."
        }), 400

    question = data.get("question")

    if not isinstance(question, str):
        return jsonify({
            "error" : "The question must be a text."
        }), 400

    question = question.strip()
    
    if not question:
        return jsonify({
            "error" : "Please enter a question."
        }), 400

    if len(question) > 2000:
        return jsonify({
            "error" : "Please keep your question within 2,000 characters."
        }), 400

    session_id = session.get("session_id")
    collection = collections.get(session_id)

    if collection is None:
        return jsonify({
            "error" : "Please upload your PDFs before asking a question."
        }), 400

    try:
        result = answer_question(collection["vector_store"], question)

    except Exception:
        app.logger.exception("Answer generation failed.")

        return jsonify({
            "error" : "The answer could not be generated. Please try again."
        }), 500

    return jsonify(result)


@app.get("/api/status")
def get_status():
    return jsonify({
        "status" : "running",
        "service" : "document-assistant",
    })

@app.errorhandler(413)
def handle_large_upload(error):
    return jsonify({
        "error" : "The upload request exceeds the 20 MiB limit."
    }), 413

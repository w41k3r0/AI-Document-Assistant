import os
from pathlib import Path
from functools import lru_cache
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(Path(__file__).parent / ".env")

@lru_cache(maxsize=1)
def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_MODEL")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing!")
    if not model_name:
        raise ValueError("GEMINI_MODEL is missing!")

    llm = ChatGoogleGenerativeAI(
        model = model_name,
        google_api_key = api_key,
        vertexai = False,
        timeout = 60,
        max_retries = 2,
    )

    return llm

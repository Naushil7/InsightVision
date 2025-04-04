import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Mistral
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY")
    MISTRAL_MODEL: str = os.getenv("MISTRAL_MODEL", "mistral-small")

    # Paths
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "data/uploads")
    INDEX_PATH: str = os.getenv("INDEX_PATH", "data/vectorstore/index.faiss")

    # Embedding
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

settings = Settings()

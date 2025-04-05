import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

# Load model once
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight, free
embedding_model = SentenceTransformer('./models/all-MiniLM-L6-v2')


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    """
    Splits text into overlapping chunks of tokens (approximated via whitespace).
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks


def embed_chunks(chunks: List[str]) -> np.ndarray:
    """
    Returns the embeddings for the given text chunks.
    """
    return embedding_model.encode(chunks, show_progress_bar=True)


def create_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    Creates a FAISS index from the given embeddings.
    """
    if embeddings.size == 0:
        raise ValueError("❌ No embeddings provided. Cannot create FAISS index.")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


def save_index(index: faiss.IndexFlatL2, path: str = "data/vectorstore/index.faiss"):
    faiss.write_index(index, path)


def load_index(path: str = "data/vectorstore/index.faiss") -> faiss.IndexFlatL2:
    return faiss.read_index(path)

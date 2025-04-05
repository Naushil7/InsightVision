import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

# Load the same embedding model used for indexing
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
embedding_model = SentenceTransformer('./models/all-MiniLM-L6-v2')


def load_faiss_index(index_path: str = "data/vectorstore/index.faiss") -> faiss.IndexFlatL2:
    """
    Loads a saved FAISS index from disk.
    """
    return faiss.read_index(index_path)


def embed_query(query: str) -> np.ndarray:
    """
    Converts a query string into an embedding vector.
    """
    embedding = embedding_model.encode([query])
    return np.array(embedding).astype("float32")


def search_index(index: faiss.IndexFlatL2, query_embedding: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Searches the FAISS index and returns distances and indices of top-k results.
    """
    distances, indices = index.search(query_embedding, top_k)
    return distances, indices

from app.services.vectorstore.vector_utils import load_faiss_index, embed_query, search_index
from app.services.vectorstore.chunk_embed import chunk_text
from app.services.extract.pdf_handler import extract_text_smart
from app.config import settings

def get_top_chunks(question: str, chunks: list, top_k: int = 3) -> str:
    index = load_faiss_index(settings.INDEX_PATH)
    q_embed = embed_query(question)
    distances, indices = search_index(index, q_embed)

    return "\n\n".join([chunks[i] for i in indices[0][:top_k]])

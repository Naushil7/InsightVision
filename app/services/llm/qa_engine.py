from app.services.vectorstore.vector_utils import load_faiss_index, embed_query, search_index
from app.services.vectorstore.chunk_embed import chunk_text
from app.services.extract.pdf_handler import extract_text_smart
from app.config import settings
from app.services.llm.mistral_client import ask_mistral

# def get_top_chunks(question: str, chunks: list, top_k: int = 3) -> str:
#     index = load_faiss_index(settings.INDEX_PATH)
#     q_embed = embed_query(question)
#     distances, indices = search_index(index, q_embed)

#     return "\n\n".join([chunks[i] for i in indices[0][:top_k]])

def ask_question(index, question, top_k=5, history=None, chunks=None):
    query_embedding = embed_query(question)
    distances, indices = search_index(index, query_embedding, top_k=top_k)

    # Get top-k matching chunks using indices
    top_results = [chunks[i] for i in indices[0] if i != -1]

    context = "\n\n".join(top_results)

    if history:
        history_block = "\n\n".join([f"Q: {item['question']}\nA: {item['answer']}" for item in history])
        context = f"{history_block}\n\n{context}"

    return ask_mistral(context, question)


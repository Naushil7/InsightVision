import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.services.extract.pdf_handler import extract_text_smart
from app.services.extract.image_handler import extract_text_from_image
from app.services.vectorstore.chunk_embed import chunk_text, embed_chunks, create_faiss_index, save_index
from app.services.vectorstore.vector_utils import embed_query, load_faiss_index, search_index
from app.services.llm.qa_engine import get_top_chunks
from app.services.llm.mistral_client import ask_mistral
from app.config import settings
from app.utils.file_ops import save_uploaded_file, get_file_type, cleanup_temp_dir

st.set_page_config(page_title="InsightVision", layout="wide")
st.title("📘 InsightVision: Understand PDFs & Images with Mistral")

uploaded_file = st.file_uploader("Upload a PDF or image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)
    file_type = get_file_type(file_path)

    if file_type == "pdf":
        text = extract_text_smart(file_path)
    elif file_type == "image":
        text = extract_text_from_image(file_path)
    else:
        st.error("❌ Unsupported file type.")
        st.stop()

    st.success("✅ File processed successfully.")

    st.text_area("Extracted Text (preview)", value=text[:1000], height=200)

    # Embed and save index
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)
    index = create_faiss_index(embeddings)
    save_index(index, settings.INDEX_PATH)

    st.success("✅ Text embedded and indexed.")

    question = st.text_input("Ask a question:")
    if question:
        top_chunks = get_top_chunks(question, chunks)
        response = ask_mistral(top_chunks, question)

        st.markdown("### 🤖 Mistral Answer:")
        st.write(response)

    cleanup_temp_dir()
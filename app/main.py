import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.services.extract.pdf_handler import extract_text_smart
from app.services.extract.image_handler import extract_text_from_image
from app.services.vectorstore.chunk_embed import chunk_text, embed_chunks, create_faiss_index, save_index
from app.services.vectorstore.vector_utils import embed_query, load_faiss_index, search_index
# from app.services.llm.qa_engine import get_top_chunks
from app.services.llm.mistral_client import ask_mistral
from app.config import settings
from app.utils.file_ops import save_uploaded_file, get_file_type, cleanup_temp_dir

from app.services.llm.qa_engine import ask_question

# Session state to keep track of chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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
        if not text or len(text.strip()) < 50:
            st.warning("🖼️ Not enough high-confidence text extracted.")
            question = st.text_input("Ask a question based on OCR result:")
            if question:
                response = ask_mistral(text, question)
                st.markdown("### 🤖 Mistral Answer:")
                st.write(response)
            st.stop()
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

    # question = st.text_input("Ask a question:")
    # if question:
    #     top_chunks = get_top_chunks(question, chunks)
    #     response = ask_mistral(top_chunks, question)

    #     st.markdown("### 🤖 Mistral Answer:")
    #     st.write(response)
    
    question = st.text_input("Ask a question about this document:")

    st.markdown("""
    <style>
        .stButton button {
            width: 100%;
            margin-right: 0px;
            padding-left: 5px;
            padding-right: 5px;
        }
        div.row-widget.stHorizontal {
            gap: 0rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Then your original button code
    button_col = st.columns(4)
    ask_button = button_col[0].button("📤 Ask")
    toggle_button = button_col[1].button("📚 Toggle History")
    reset_button = button_col[2].button("🔁 Clear Chat")
    reset_page_button = button_col[3].button("🔄 Reset Page")

    # Action: Reset Chat
    if reset_button:
        st.session_state.chat_history = []
        st.success("✅ Chat history reset.")
        st.stop()
        
    # Action: Reset Page
    if reset_page_button:
        st.session_state.chat_history = []
        st.session_state.clear()
        st.experimental_rerun()

    # Action: Ask
    if ask_button and question:
        answer = ask_question(index, question, top_k=5, history=st.session_state.chat_history, chunks=chunks)
        st.session_state.chat_history.append({
            "question": question,
            "answer": answer
        })

    # Show/hide toggle flag
    if "show_history" not in st.session_state:
        st.session_state.show_history = True

    if toggle_button:
        st.session_state.show_history = not st.session_state.show_history

    # Show chat history if enabled
    if st.session_state.get("show_history") and st.session_state.chat_history:
        st.markdown("### 🤖 Mistral Answer:")
        for qa in st.session_state.chat_history:
            st.markdown(f"**Q:** {qa['question']}")
            st.markdown(f"**A:** {qa['answer']}")
            st.markdown("---")
    elif st.session_state.get("show_history") and len(st.session_state.chat_history) > 1:
        # If there's only 1 response, just show it without "Chat History" heading
        last = st.session_state.chat_history[-1]
        st.markdown("### 🤖 Mistral Answer with 💬 Chat History")
        st.markdown(f"**Q:** {last['question']}")
        st.markdown(f"**A:** {last['answer']}")
            
    cleanup_temp_dir()
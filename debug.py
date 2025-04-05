# # debug.py

# from app.services.extract.pdf_handler import extract_text_smart
# from app.services.extract.image_handler import extract_text_from_image
# from app.services.vectorstore.chunk_embed import chunk_text, embed_chunks, create_faiss_index, save_index
# from app.services.vectorstore.vector_utils import load_faiss_index, embed_query, search_index
# from app.services.vectorstore.chunk_embed import chunk_text
# from app.services.extract.pdf_handler import extract_text_smart
# from app.services.llm.mistral_client import ask_mistral
# from app.services.llm.qa_engine import get_top_chunks
# from app.utils.file_ops import save_uploaded_file, get_file_type, cleanup_temp_dir
# from app.config import settings
# import os

# def test_pdf_extraction():
#     path = "./data/temp/Resume_DS_v2.pdf"
#     if not os.path.exists(path):
#         print(f"❌ File not found: {path}")
#         return
#     text = extract_text_smart(path)
#     print(f"✅ Extracted PDF Text (first 500 chars):\n{text[:500]}")

# def test_image_extraction():
#     path = "./data/temp/trial.png"
#     if not os.path.exists(path):
#         print(f"❌ File not found: {path}")
#         return
#     text = extract_text_from_image(path)
#     print(f"✅ Extracted Image Text (first 500 chars):\n{text[:500]}")

# def test_embedding_pipeline():
#     path = "./data/temp/Resume_DS_v2.pdf"
#     from app.services.extract.pdf_handler import extract_text_smart
#     text = extract_text_smart(path)

#     print("🔹 Chunking text...")
#     chunks = chunk_text(text)
#     print(f"🔸 Total chunks: {len(chunks)}")

#     print("🔹 Embedding chunks...")
#     embeddings = embed_chunks(chunks)

#     print("🔹 Creating FAISS index...")
#     index = create_faiss_index(embeddings)
#     save_index(index)
#     print("✅ Index saved to 'data/vectorstore/index.faiss'")
    
# def test_query_search():
#     query = "What machine learning frameworks has the candidate used?"
#     index = load_faiss_index()
#     query_embedding = embed_query(query)
#     distances, indices = search_index(index, query_embedding)

#     # Retrieve original text chunks to show matching results
#     pdf_text = extract_text_smart("./data/temp/Resume_DS_v2.pdf")
#     chunks = chunk_text(pdf_text)

#     print("🔍 Top Matches:\n")
#     for i, idx in enumerate(indices[0]):
#         print(f"#{i+1} | Score: {distances[0][i]:.2f}")
#         print(chunks[idx])
#         print("-" * 50)

# def test_llm_answer():
#     query = "What machine learning frameworks has the candidate used?"
#     index = load_faiss_index()
#     query_embedding = embed_query(query)
#     distances, indices = search_index(index, query_embedding)

#     # Grab top-3 chunks as context
#     pdf_text = extract_text_smart("./data/temp/Resume_DS_v2.pdf")
#     chunks = chunk_text(pdf_text)
#     context = "\n\n".join([chunks[i] for i in indices[0][:3]])

#     print("\n🤖 Asking Mistral...\n")
#     answer = ask_mistral(context, query)
#     print(f"🧠 Answer:\n{answer}")

# def test_qa_engine_with_pdf():
#     print("🔹 Testing QA pipeline with PDF...")

#     file_path = "./data/temp/Resume_DS_v2.pdf"
#     text = extract_text_smart(file_path)
#     chunks = chunk_text(text)
#     embeddings = embed_chunks(chunks)
#     index = create_faiss_index(embeddings)
#     save_index(index)

#     question = "What machine learning frameworks has the candidate used?"
#     top_context = get_top_chunks(question, chunks)
#     response = ask_mistral(top_context, question)

#     print("✅ Question:", question)
#     print("🧠 Mistral Answer:", response)

# def test_file_ops():
#     print("🔹 Testing file operations...")

#     dummy_file = "./data/temp/Resume_DS_v2.pdf"
#     uploaded_name = "test_resume.pdf"

#     # Simulate file save
#     with open(dummy_file, "rb") as f:
#         buffer = f.read()

#     class FakeUpload:
#         name = uploaded_name
#         def getbuffer(self): return buffer

#     path = save_uploaded_file(FakeUpload())
#     print(f"✅ File saved to: {path}")
#     print(f"📄 File type: {get_file_type(path)}")

#     cleanup_temp_dir()
#     print("🧹 Temp folder cleaned.")


# if __name__ == "__main__":
#     print("🔍 Running PDF/Text Extraction Tests...\n")
#     # test_pdf_extraction()
#     # print("\n" + "-"*60 + "\n")
#     # test_image_extraction()
#     # print("\n" + "-"*60 + "\n")
#     # test_embedding_pipeline()
#     # test_query_search()
#     # test_llm_answer()
#     test_qa_engine_with_pdf()
#     print("\n" + "-" * 60 + "\n")
#     test_file_ops()
    


from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
model.save('./models/all-MiniLM-L6-v2')




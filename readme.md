# InsightVision

![Status](https://img.shields.io/badge/status-deployed-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue) ![GCP](https://img.shields.io/badge/deployed%20on-Google%20Cloud%20Run-orange)

🔗 **Live App**: [https://insightvision-18564642412.us-central1.run.app](https://insightvision-18564642412.us-central1.run.app)

> InsightVision is a lightweight, cloud-deployable document understanding tool that extracts content from PDFs or images, semantically indexes it using embeddings, and allows LLM-powered question answering using Mistral.

---

## 🧠 Project Explanation

### 🤔 Why Not Just Use an LLM Directly on PDFs?

While LLMs like OpenAI’s GPT-4 can ingest PDFs directly, InsightVision is built with a more **structured and scalable pipeline** where the LLM plays a focused role:

- ✅ The **LLM is not responsible for everything** — it’s only used at the end for answering questions.
- 🔍 All the **heavy lifting (text extraction, cleaning, chunking, semantic search)** is done **before** the LLM is called.
- 🧠 This means:
  - Lower token usage (cheaper, faster)
  - More contextually relevant answers
  - Better explainability and modularity

In contrast, uploading a PDF to an LLM treats the model as a black box — which might work for summaries, but falls short for precise querying, scalable architecture, and image-based documents.

While it's tempting to directly send an entire PDF to an LLM, this approach has major limitations:

- **Token Limits**: Most LLM APIs have strict context length restrictions (e.g., 4K to 32K tokens). Long PDFs easily exceed this.
- **No Indexing**: LLMs don't inherently "understand" document structure or let you query specific parts semantically.
- **OCR Blindness**: LLMs cannot process raw image scans or scanned text in PDFs.
- **No Reuse**: Each query is a cold start — there's no persistent understanding or index.

**InsightVision solves all of these** by:
- Extracting and chunking text intelligently
- Using **FAISS** to find only the most relevant content
- Feeding only top-matching chunks into the LLM
- Supporting **images and scanned PDFs** via OCR
- Running offline-ready with local embeddings

This pipeline is faster, smarter, more scalable, and cost-efficient than raw LLM usage.


InsightVision was created to combine robust document understanding with the power of large language models — especially for analyzing resumes, scanned documents, academic PDFs, and images.

### What it does:
- Allows users to upload PDFs and images
- Extracts high-quality text (with OCR fallback for images)
- Embeds the extracted content using `SentenceTransformer`
- Stores and searches via FAISS for semantic similarity
- Passes top-matched context to the **Mistral API** to answer questions
- Deployed as a **serverless Streamlit app on Google Cloud Run**

This project emphasizes modularity, offline resilience (local model), and clean UI/UX via Streamlit. It’s designed to be both a robust ML pipeline and a showcase-ready portfolio project.

---

## 🖼️ Dashboard Preview

![InsightVision UI](data/temp/Dashborad_Image.png)

---

## 🚀 Features

- 📄 PDF and 🖼️ image (OCR) support
- 🔍 FAISS-based vector search for semantic matching
- 🤖 Mistral LLM integration for intelligent answers
- 🧠 Smart OCR fallback and captioning-ready design
- ☁️ Dockerized & deployable on GCP (Cloud Run)
- 🖥️ Streamlit frontend

---

## 📦 Folder Structure

```bash
insightvision/
├── app/
│   ├── main.py                  # Streamlit frontend
│   ├── config.py                # Environment setup
│   ├── services/
│   │   ├── extract/             # PDF and image handlers
│   │   ├── vectorstore/         # Chunking, embedding, FAISS
│   │   └── llm/                 # Mistral API integration
│   ├── routes/                  # (Optional FastAPI backend)
│   ├── utils/                   # file_ops, helpers
├── models/                     # Pre-downloaded embedding model
├── data/                       # Uploaded files + FAISS index
├── .env                        # API keys and configs
├── Dockerfile
├── requirements.txt
├── README.md
└── run_local.sh
```

---

## 🧠 Project Workflow (Mermaid)

```mermaid
flowchart TD
  A[User Uploads File] --> B{File Type?}
  B -->|PDF| C[Extract PDF Text]
  B -->|Image| D[OCR Extraction]
  C & D --> E[Chunk & Embed]
  E --> F[FAISS Index/Search]
  G[User Asks Question] --> F
  F --> H[Retrieve Top Matches]
  H --> I[Mistral API]
  I --> J[Answer Shown on UI]
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/InsightVision.git
cd InsightVision
```

### 2. Setup Environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Add `.env`
```env
MISTRAL_API_KEY=your-api-key
UPLOAD_DIR=data/uploads
INDEX_PATH=data/vectorstore/index.faiss
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 4. Run Locally
```bash
streamlit run app/main.py
```

---

## 🐳 Docker Instructions

### Build Locally
```bash
docker build -t insightvision .
```

### Run Locally
```bash
docker run -p 8080:8080 --env-file .env insightvision
```

### Deploy to GCP
```bash
gcloud run deploy insightvision \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT/insightvision-repo/insightvision \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --set-env-vars MISTRAL_API_KEY=your-key
```

---

## 🤝 Future Enhancements
- 🔄 Add support for BLIP-based image captioning
- 🧩 Plug-in integration for LangChain or ChromaDB
- 🧠 Citation generation using RAG
- 🗂️ Multi-file ingestion and Q&A

---

## 📄 License

MIT License. Use freely and contribute back!

---
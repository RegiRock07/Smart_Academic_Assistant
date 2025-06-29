# 🎓 Smart Academic Assistant

The **Smart Academic Assistant** is an intelligent tool built using a Retrieval-Augmented Generation (RAG) pipeline. It allows students to upload academic documents (PDF, DOCX, TXT) and get structured, instant answers powered by open-source LLMs via Groq. It includes an interactive Streamlit interface and supports advanced agentic workflows.

## 🚀 Features

- 📄 Upload and process PDF, DOCX, or TXT files
- 🔍 Context-aware Question Answering using RAG
- 🧠 Fast and efficient LLM responses via Groq-hosted models (Mixtral, LLaMA3, Gemma)
- 🧩 Modular tools like:
  - Summarize Document
  - Generate MCQs
  - Topic-wise Explanations
- 🧠 Conversational Retrieval using `ConversationalRetrievalChain`
- 🌐 Beautiful and responsive Streamlit UI
- 📦 Local FAISS vector store for embeddings

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** LangChain, Python
- **Vector DB:** FAISS
- **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
- **LLMs:** Open-source models via [Groq](https://console.groq.com/)
- **Document Loaders:** LangChain Community Loaders

---



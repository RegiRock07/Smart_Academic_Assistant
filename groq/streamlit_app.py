import streamlit as st
import time
import os
import tempfile
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
#from langchain.agents import Tool, initialize_agent, AgentType

# -------------------- Page Configuration --------------------
st.set_page_config(page_title="Smart Academic Assistant", layout="centered")

# -------------------- Theme Toggle -------------------- (Not Working)
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.sidebar.toggle("🌙 Dark Mode", key="dark_mode")
if st.session_state.dark_mode:
    st.markdown("""
        <style>
            body {
                background-color: #121212;
                color: #ffffff;
            }
            .stTextInput>div>div>input {
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)
# -------------------- Model Settings --------------------
st.sidebar.header("🧠 Model Configuration")

model_name = st.sidebar.selectbox(
    "Select AI Model:",
    ["llama3-70b-8192", "llama3-8b-8192", "gemma-7b-it", "mixtral-8x22b"],
    index=0
)
temperature = st.sidebar.slider("Creativity (Temperature):", 0.0, 1.0, 0.5, step=0.01)
max_tokens = st.sidebar.slider("Max Response Length:", 512, 8192, 3072, step=64)

# -------------------- Title --------------------
st.title("📚 Smart Academic Assistant")
st.write("Upload your academic documents and ask questions to get structured answers.")

# -------------------- File Upload Section --------------------
uploaded_files = st.file_uploader(
    "📄 Upload Documents (PDF, DOCX, or TXT):",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# -------------------- Question Input --------------------
question = st.text_input("🔍 Enter your question:")

# -------------------- Submit Button --------------------
if st.button("🧠 Get Answer"):
    if not uploaded_files or not question:
        st.warning("⚠️ Please upload at least one document and enter a question.")
    else:
        load_dotenv()
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            st.error("🚨 GROQ_API_KEY not found in your environment.")
            st.stop()

        raw_docs = []
        for i, file in enumerate(uploaded_files):
            suffix = file.name.split(".")[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            with st.spinner(f"📖 Reading and interpreting ‘{file.name}’..."):
                time.sleep(0.75 + i * 0.25)
                try:
                    if suffix == "pdf":
                        loader = PyPDFLoader(tmp_path)
                    elif suffix == "docx":
                        loader = Docx2txtLoader(tmp_path)
                    elif suffix == "txt":
                        loader = TextLoader(tmp_path)
                    else:
                        st.warning(f"❌ Unsupported file format: {suffix}")
                        continue
                    raw_docs.extend(loader.load())
                finally:
                    os.remove(tmp_path)

        if not raw_docs:
            st.warning("❌ No valid documents to process.")
            st.stop()

        with st.spinner("🔄 🔍 Consulting the academic oracle... please wait ✨"):
            splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
            chunks = splitter.split_documents(raw_docs)
            st.session_state.chunks = chunks

            embed_progress = st.progress(0, text="🔗 Converting documents to embeddings...")
            for i in range(3):
                time.sleep(0.3)
                embed_progress.progress((i + 1) / 3.0)

            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vector_store = FAISS.from_documents(chunks, embeddings)
            retriever = vector_store.as_retriever()

            prompt = ChatPromptTemplate.from_template("""
            You are a helpful academic assistant. Use the context below to answer the question.

            <context>
            {context}
            </context>

            Question: {input}
            Provide a clear and helpful answer.
            """)

            llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
            st.session_state.llm = llm

            document_chain = create_stuff_documents_chain(llm, prompt)
            retrieval_chain = create_retrieval_chain(retriever, document_chain)

            start = time.time()
            response = retrieval_chain.invoke({"input": question})
            end = time.time()

            answer = response.get("answer", "No answer generated.")
            context_docs = response.get("context", chunks)
            source_doc = "Uploaded Document"

            if context_docs:
                source_doc = context_docs[0].metadata.get("source", "Uploaded Document")

            confidence_score = round(min(1.0, 0.95 - 0.05 * len(context_docs)), 2)

            structured_response = {
                "question": question,
                "answer": answer,
                "source_document": os.path.basename(source_doc),
                "confidence_score": str(confidence_score)
            }
            st.subheader("🎓 Your Answer:")
            st.json(structured_response)
            st.caption(f"⏱️ Answer generated in {round(end - start, 2)} seconds")
            
# -------------------- Agentic Tools --------------------
if "chunks" in st.session_state and "llm" in st.session_state:
    chunks = st.session_state.chunks
    llm = st.session_state.llm

    def run_chain(template, input_text):
        prompt = ChatPromptTemplate.from_template(template)
        return (prompt | llm).invoke({"input": input_text}).content

    st.markdown("---")
    st.subheader("🧰 Extra Learning Utilities")

    col1, col2, col3 = st.columns(3)

    summary, mcqs, explanation = None, None, None
    doc_content = chunks[0].page_content if chunks else ""

    with col1:
        if st.button("📑 Summarize Document"):
            with st.spinner("Generating summary..."):
                summary = run_chain("Summarize the following academic content clearly:\n{input}", doc_content)

    with col2:
        if st.button("📝 Generate MCQs"):
            with st.spinner("Generating MCQs..."):
                mcqs = run_chain(
                    "Generate 3 MCQs from the following content with 4 options each and mark the correct one:\n{input}",
                    doc_content
                )

    with col3:
        if st.button("📚 Topic-wise Explanation"):
            with st.spinner("Generating explanation..."):
                explanation = run_chain("Provide a simple topic-wise explanation of:\n{input}", doc_content)


    if summary:
        with st.expander("📄 Document Summary", expanded=True):
            st.markdown(summary)
            st.download_button("📥 Download Summary", summary, file_name="summary.txt", mime="text/plain")

    if mcqs:
        with st.expander("🧠 Practice Questions", expanded=True):
            st.markdown(mcqs)
            st.download_button("📥 Download MCQs", mcqs, file_name="mcqs.txt", mime="text/plain")

    if explanation:
        with st.expander("🔍 Topic-wise Explanation", expanded=True):
            st.markdown(explanation)
            st.download_button("📥 Download Explanation", explanation, file_name="explanation.txt", mime="text/plain")

# -------------------- Footer --------------------
st.markdown("---")
st.caption("Mentox Bootcamp · Final Capstone Project · Phase 1")

# ==================== IMPORTS ====================
import streamlit as st
import time
import os
import tempfile
from dotenv import load_dotenv

# LangChain imports for document processing and AI
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# PDF generation imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

# Import your custom theme module
from ui_themes import setup_theme_system

# ==================== PDF CREATION FUNCTION ====================
def create_pdf_summary(summary_text, title="Document Summary"):
    """
    Convert summary text to PDF format with professional styling
    
    Args:
        summary_text (str): The text content to convert to PDF
        title (str): The title for the PDF document
    
    Returns:
        bytes: PDF file content as bytes
    """
    # Create a BytesIO buffer to store PDF content
    buffer = io.BytesIO()
    
    # Create PDF document with letter page size and 1-inch top margin
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch)
    
    # Get default styles and create custom title style
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor='Black'  
    )
    
    # Build PDF content
    story = []
    story.append(Paragraph(title, title_style))  # Add title
    story.append(Spacer(1, 20))  # Add space after title
    # Convert newlines to HTML breaks for proper PDF formatting
    story.append(Paragraph(summary_text.replace('\n', '<br/>'), styles['Normal']))
    
    # Generate PDF and return as bytes
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(page_title="Smart Academic Assistant", layout="centered")

# ==================== APPLY THEME SYSTEM ====================
setup_theme_system()

# ==================== MODEL SETTINGS SIDEBAR ====================
st.sidebar.header("🧠 Model Configuration")

# AI Model selection dropdown
model_name = st.sidebar.selectbox(
    "Select AI Model:",
    ["llama3-70b-8192", "llama3-8b-8192", "gemma-7b-it", "mixtral-8x22b"],
    index=0  # Default to first option
)

# Temperature slider for creativity control
temperature = st.sidebar.slider("Creativity (Temperature):", 0.0, 1.0, 0.5, step=0.01)

# Max tokens slider for response length control
max_tokens = st.sidebar.slider("Max Response Length:", 512, 8192, 3072, step=64)

# ==================== MAIN TITLE ====================
st.title("📚 Smart Academic Assistant")
st.write("Upload your academic documents and ask questions to get structured answers.")

# ==================== FILE UPLOAD SECTION ====================
# Multiple file uploader for different document types
uploaded_files = st.file_uploader(
    "📄 Upload Documents (PDF, DOCX, or TXT):",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# ==================== QUESTION INPUT ====================
# Text input for user's question
question = st.text_input("🔍 Enter your question:")

# ==================== MAIN PROCESSING SECTION ====================
# Submit button to trigger document processing and Q&A
if st.button("🧠 Get Answer"):
    # Validation: Check if files and question are provided
    if not uploaded_files or not question:
        st.warning("⚠️ Please upload at least one document and enter a question.")
    else:
        # Load environment variables (for API keys)
        load_dotenv()
        groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Check if API key exists
        if not groq_api_key:
            st.error("🚨 GROQ_API_KEY not found in your environment.")
            st.stop()

        # ==================== DOCUMENT LOADING ====================
        raw_docs = []  # List to store all loaded documents
        
        # Process each uploaded file
        for i, file in enumerate(uploaded_files):
            # Get file extension to determine loader type
            suffix = file.name.split(".")[-1]
            
            # Create temporary file for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            # Load document with appropriate loader and show progress
            with st.spinner(f"📖 Reading and interpreting '{file.name}'..."):
                time.sleep(0.75 + i * 0.25)  # Simulate processing time
                try:
                    # Select appropriate document loader based on file type
                    if suffix == "pdf":
                        loader = PyPDFLoader(tmp_path)
                    elif suffix == "docx":
                        loader = Docx2txtLoader(tmp_path)
                    elif suffix == "txt":
                        loader = TextLoader(tmp_path)
                    else:
                        st.warning(f"❌ Unsupported file format: {suffix}")
                        continue
                    
                    # Load and add documents to collection
                    raw_docs.extend(loader.load())
                finally:
                    # Clean up temporary file
                    os.remove(tmp_path)

        # Check if any documents were successfully loaded
        if not raw_docs:
            st.warning("❌ No valid documents to process.")
            st.stop()

        # ==================== DOCUMENT PROCESSING & RETRIEVAL ====================
        with st.spinner("🔄 🔍 Consulting the academic oracle... please wait ✨"):
            # Split documents into smaller chunks for better processing
            splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
            chunks = splitter.split_documents(raw_docs)
            st.session_state.chunks = chunks  # Store for later use

            # Show embedding progress with progress bar
            embed_progress = st.progress(0, text="🔗 Converting documents to embeddings...")
            for i in range(3):
                time.sleep(0.3)
                embed_progress.progress((i + 1) / 3.0)

            # Create embeddings and vector store for similarity search
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vector_store = FAISS.from_documents(chunks, embeddings)
            retriever = vector_store.as_retriever()

            # ==================== AI CHAIN SETUP ====================
            # Create prompt template for the AI model
            prompt = ChatPromptTemplate.from_template("""
            You are a helpful academic assistant. Use the context below to answer the question.

            <context>
            {context}
            </context>

            Question: {input}
            Provide a clear and helpful answer.
            """)

            # Initialize the language model with user settings
            llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
            st.session_state.llm = llm  # Store for later use

            # Create document processing and retrieval chains
            document_chain = create_stuff_documents_chain(llm, prompt)
            retrieval_chain = create_retrieval_chain(retriever, document_chain)

            # ==================== GENERATE ANSWER ====================
            # Measure response time
            start = time.time()
            response = retrieval_chain.invoke({"input": question})
            end = time.time()

            # Extract response components
            answer = response.get("answer", "No answer generated.")
            context_docs = response.get("context", chunks)
            source_doc = "Uploaded Document"

            # Get source document name if available
            if context_docs:
                source_doc = context_docs[0].metadata.get("source", "Uploaded Document")

            # Calculate confidence score (simplified estimation)
            confidence_score = round(min(1.0, 0.95 - 0.05 * len(context_docs)), 2)

            # ==================== DISPLAY RESULTS ====================
            # Structure the response for display
            structured_response = {
                "question": question,
                "answer": answer,
                "source_document": os.path.basename(source_doc),
                "confidence_score": str(confidence_score)
            }
            
            # Display the answer in JSON format
            st.subheader("🎓 Your Answer:")
            st.json(structured_response)
            st.caption(f"⏱️ Answer generated in {round(end - start, 2)} seconds")
            
# ==================== AGENTIC TOOLS SECTION ====================
# Additional utilities that become available after document processing
if "chunks" in st.session_state and "llm" in st.session_state:
    # Get stored chunks and language model from session state
    chunks = st.session_state.chunks
    llm = st.session_state.llm

    def run_chain(template, input_text):
        """
        Helper function to run a simple prompt-LLM chain
        
        Args:
            template (str): Prompt template with {input} placeholder
            input_text (str): Text to process
        
        Returns:
            str: Generated response from the language model
        """
        prompt = ChatPromptTemplate.from_template(template)
        return (prompt | llm).invoke({"input": input_text}).content

    # ==================== UTILITY TOOLS UI ====================
    st.markdown("---")
    st.subheader("🧰 Extra Learning Utilities")

    # Create three columns for different tools
    col1, col2, col3 = st.columns(3)

    # Initialize variables to store generated content
    summary, mcqs, explanation = None, None, None
    
    # Get first chunk content for processing (or empty string if no chunks)
    doc_content = chunks[0].page_content if chunks else ""

    # ==================== TOOL BUTTONS ====================
    # Column 1: Document Summarization
    with col1:
        if st.button("📑 Summarize Document"):
            with st.spinner("Generating summary..."):
                summary = run_chain(
                    "Summarize the following academic content clearly:\n{input}", 
                    doc_content
                )

    # Column 2: MCQ Generation
    with col2:
        if st.button("📝 Generate MCQs"):
            with st.spinner("Generating MCQs..."):
                mcqs = run_chain(
                    "Generate 3 MCQs from the following content with 4 options each and mark the correct one:\n{input}",
                    doc_content
                )

    # Column 3: Topic-wise Explanation
    with col3:
        if st.button("📚 Topic-wise Explanation"):
            with st.spinner("Generating explanation..."):
                explanation = run_chain(
                    "Provide a simple topic-wise explanation of:\n{input}", 
                    doc_content
                )

    # ==================== DISPLAY GENERATED CONTENT ====================
    # Display Summary with PDF download option
    if summary:
        with st.expander("📄 Document Summary", expanded=True):
            st.markdown(summary)
            # Generate PDF and create download button
            pdf_data = create_pdf_summary(summary, "Document Summary")
            st.download_button(
                "📥 Download Summary", 
                pdf_data, 
                file_name="summary.pdf", 
                mime="application/pdf"
            )

    # Display MCQs with PDF download option
    if mcqs:
        with st.expander("🧠 Practice Questions", expanded=True):
            st.markdown(mcqs)
            # Generate PDF and create download button
            pdf_data = create_pdf_summary(mcqs, "Practice Questions")
            st.download_button(
                "📥 Download MCQs", 
                pdf_data, 
                file_name="mcqs.pdf", 
                mime="application/pdf"
            )

    # Display Explanation with PDF download option
    if explanation:
        with st.expander("🔍 Topic-wise Explanation", expanded=True):
            st.markdown(explanation)
            # Generate PDF and create download button
            pdf_data = create_pdf_summary(explanation, "Topic-wise Explanation")
            st.download_button(
                "📥 Download Explanation", 
                pdf_data, 
                file_name="explanation.pdf", 
                mime="application/pdf"
            )

# ==================== FOOTER ====================
st.markdown("---")
st.caption("Mentox Bootcamp · Final Capstone Project · Phase 1")
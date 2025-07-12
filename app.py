import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader, JSONLoader
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()  # Load environment variables from .env file


# Function to load and split document
def process_file(uploaded_file):
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    # Detect file type
    if uploaded_file.name.endswith(".pdf"):
        loader = PyPDFDirectoryLoader(os.path.dirname(file_path))
    elif uploaded_file.name.endswith(".json"):
        loader = JSONLoader(file_path=file_path, jq_schema=".data", text_content=False)
    else:
        st.error("Unsupported file format. Please upload a PDF or JSON file.")
        return None

    docs = loader.load()

    # Split into chunks
    char_text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return char_text_splitter.split_documents(docs)

# Initialize LLM and Embeddings (this can be optimized to cache)
def init_llm():
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.0,
       
        verbose=True,
    )
    return embedding_function, llm

# Streamlit App UI
def main():
    st.title("Document Q&A ")

    uploaded_file = st.file_uploader("Upload your PDF or JSON file", type=["pdf", "json"])
    if uploaded_file:
        st.success(f"Uploaded {uploaded_file.name}")
        doc_texts = process_file(uploaded_file)
        embedding_function, llm = init_llm()

        # Create Vector Store
        vstore = Chroma.from_documents(doc_texts, embedding_function)

        retriever = vstore.as_retriever()

        # QnA section
        question = st.text_input("Ask a question based on the uploaded document:")
        if question:
            # Retrieve relevant docs
            retrieved_context = retriever.get_relevant_documents(question)
            combined_context = " ".join([doc.page_content for doc in retrieved_context])
            input_text = f"Question: {question}\n\nContext: {combined_context}\n\nAnswer:"

            response = llm.invoke(input_text)
            answer = response.content
            st.write("### Answer:")
            st.write(answer)
if __name__ == "__main__":
    main()

# 📄 Document Q&A App 

An intelligent Q&A tool that allows users to upload `.pdf` or `.json` files and ask natural language questions about the document.

This application uses:
- 🧠 HuggingFace MiniLM for text embeddings
- 🗃️ ChromaDB to store and search document vectors
- 🔗 LangChain to chain together document loaders, embedding models, and LLMs
- ⚡ Groq’s blazing-fast LLaMA 3.1-8B for Q&A responses
- 🌐 Streamlit for an easy-to-use web interface

---
### Tech Stack
| Component       | Library / Service          |
| --------------- | -------------------------- |
| UI Framework    | Streamlit                  |
| LLM             | Groq (LLaMA 3.1-8B)        |
| Embedding Model | HuggingFace MiniLM         |
| Vector Store    | ChromaDB                   |
| Chain Logic     | LangChain                  |
| Document Loader | LangChain PDF & JSONLoader |



## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

git clone https://github.com/battu2n/DocAnalyzer-.git
cd DocAnalyzer-

### 2️⃣ Create a Virtual Environment

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

### 3️⃣ Install Dependencies

pip install -r requirements.txt

### 4️⃣ Create a .env File

Create a .env file in the root folder and add your Groq API key:

GROQ_API_KEY=your_groq_api_key


## Run the App

streamlit run app.py


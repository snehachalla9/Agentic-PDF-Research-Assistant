# PDF RAG Chatbot

A Retrieval-Augmented Generation (RAG) based PDF Question Answering application built using Streamlit, ChromaDB, and Large Language Models.

## Features

* Upload one or more PDF documents
* Automatic PDF text extraction
* Intelligent text chunking
* Vector embeddings generation
* ChromaDB vector storage
* Semantic retrieval of relevant chunks
* LLM-powered question answering
* Interactive Streamlit user interface

## Project Structure

```text
pdf-rag-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
│
├── utils/
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriver.py
│   └── llm.py
│
└── chroma_db/
```

## Tech Stack

* Python
* Streamlit
* ChromaDB
* LangChain
* Sentence Transformers
* Groq LLM / OpenAI (depending on configuration)
* PyPDF

## Installation

Clone the repository:

```bash
git clone https://github.com/snehachalla9/PDF-RAG-CHATBOT.git
cd PDF-RAG-CHATBOT
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

## Workflow

1. Upload PDF documents.
2. Extract text from PDFs.
3. Split text into chunks.
4. Generate embeddings.
5. Store embeddings in ChromaDB.
6. Retrieve relevant chunks based on user queries.
7. Generate answers using the LLM.

## Example Use Cases

* Research paper Q&A
* Academic document analysis
* Company policy document search
* Resume and report analysis
* Knowledge base chatbot

## Deployment

The application can be deployed on:

* Streamlit Community Cloud
* Render
* Hugging Face Spaces

## Author

Sneha Challa

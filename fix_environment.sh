#!/bin/bash
# fix_environment.sh

echo "🔧 Fixing Python environment for RAG project..."

# Activate venv
source /home/rgukt-basar/Music/pdf-rag-chatbot/venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Uninstall problematic packages
echo "📦 Removing old packages..."
pip uninstall langchain langchain-community langchain-core -y

# Install correct versions
echo "📦 Installing compatible versions..."
pip install langchain==0.1.0
pip install langchain-community==0.1.0
pip install langchain-core==0.1.0

# Install dependencies
pip install pydantic==1.10.13
pip install sentence-transformers==2.2.2
pip install chromadb==0.4.22
pip install streamlit==1.28.0
pip install pypdf==3.17.4
pip install langgraph==0.0.15

# Install other dependencies
pip install torch transformers tokenizers

echo "✅ Environment fixed! Run 'streamlit run app.py' to start"
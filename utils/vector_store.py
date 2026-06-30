# utils/vector_store.py
from langchain_community.vectorstores import Chroma
import chromadb
import os

def create_vectorstore(chunks, embeddings):
    """
    Create a Chroma vector store from document chunks.
    """
    try:
        # Try the new API (ChromaDB >= 0.5.0)
        # Use persistent client with proper settings
        db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="./chroma_db",  # Add this to persist
            collection_name="pdf_collection"
        )
        return db
        
    except Exception as e:
        print(f"⚠️ Error with standard Chroma creation: {e}")
        
        try:
            # Fallback: Use older API
            db = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory="./chroma_db"
            )
            return db
            
        except Exception as e2:
            print(f"⚠️ Fallback also failed: {e2}")
            
            # Final fallback: Create a temporary in-memory Chroma
            try:
                # Use the new client directly
                from chromadb.config import Settings
                
                client = chromadb.Client(Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory="./chroma_db",
                    anonymized_telemetry=False
                ))
                
                db = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings,
                    client=client,
                    collection_name="pdf_collection"
                )
                return db
                
            except Exception as e3:
                print(f"❌ All Chroma creation methods failed: {e3}")
                raise ValueError(f"Could not create vector store: {e3}")
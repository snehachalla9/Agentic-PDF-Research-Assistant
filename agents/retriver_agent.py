# """
# Retriever Agent - Phase 5 Multi-Agent System
# Version: 2.0 (Integrated with existing RAG pipeline)
# Purpose: Retrieve relevant documents using existing retrieval functions
# """

# from typing import TypedDict, List, Optional, Dict, Any
# import sys
# import os

# # Add parent directory to path for imports
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # Import YOUR EXISTING retrieval functions from your app
# try:
#     from utils.retriver import retrieve_documents
#     from utils.hybrid_retriver import hybrid_retrieve
#     from utils.reranker import rerank_documents
# except ImportError as e:
#     print(f"⚠️ Error importing retrieval functions: {e}")
#     raise


# class AgentState(TypedDict):
#     """State maintained across all agents in the LangGraph workflow"""
#     query: str
#     task: str
#     plan: List[str]
#     db: Any
#     chunks: List[Any]
#     retrieved_docs: Optional[List[Any]]
#     research_output: Optional[str]
#     final_answer: Optional[str]


# def retriever_agent(state: AgentState) -> Dict:
#     """
#     Retriever Agent: Retrieves relevant documents using existing RAG pipeline.
    
#     Task-specific retrieval configurations:
#         - question_answering: k=20, rerank to 3 (default)
#         - summary: All chunks (no retrieval needed)
#         - research_gap: k=20, rerank to default
#         - comparison: k=30, rerank to 15
#         - literature_review: k=40, rerank to 20
#         - citation: k=25, rerank to 12
#     """
    
#     query = state["query"]
#     task = state["task"]
#     plan = state.get("plan", [])
    
#     # Get the vector database and chunks from state
#     db = state.get("db")
#     chunks = state.get("chunks")
    
#     if db is None:
#         print("❌ Error: No vector database found in state")
#         return {
#             "query": query,
#             "task": task,
#             "plan": plan,
#             "db": db,
#             "chunks": chunks,
#             "retrieved_docs": [],
#             "research_output": None,
#             "final_answer": None
#         }
    
#     print(f"🔍 Retriever Agent: Processing task: {task}")
#     print(f"   Query: {query}")
    
#     # Determine retrieval strategy based on task
#     try:
#         if task == "summary":
#             # For summarization, use all chunks (no retrieval)
#             retrieved_docs = chunks
#             print(f"   📄 Using all {len(chunks)} chunks for summarization")
            
#         elif task == "question_answering":
#             # Standard retrieval: k=20, rerank to 3
#             retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=20, rerank_k=3)
            
#         elif task == "research_gap":
#             # Research gaps: k=20, default rerank
#             retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=20, rerank_k=None)
            
#         elif task == "comparison":
#             # Comparison: k=30, rerank to 15
#             retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=30, rerank_k=15)
            
#         elif task == "literature_review":
#             # Literature review: k=40, rerank to 20
#             retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=40, rerank_k=20)
            
#         elif task == "citation":
#             # Citation: k=25, rerank to 12
#             retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=25, rerank_k=12)
            
#         else:
#             # Default: standard retrieval
#             retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=20, rerank_k=3)
            
#         print(f"   ✅ Retrieved {len(retrieved_docs)} documents")
        
#     except Exception as e:
#         print(f"   ❌ Retrieval failed: {e}")
#         retrieved_docs = []
    
#     # Update state with retrieved documents
#     return {
#         "query": query,
#         "task": task,
#         "plan": plan,
#         "db": db,
#         "chunks": chunks,
#         "retrieved_docs": retrieved_docs,
#         "research_output": None,
#         "final_answer": None
#     }


# # --------------------------------------------------------------------
# # Helper Functions
# # --------------------------------------------------------------------

# def _retrieve_with_hybrid(db: Any, chunks: List[Any], query: str, retrieval_k: int = 20, rerank_k: int = None) -> List[Dict]:
#     """
#     Retrieve documents using hybrid search and optional reranking.
#     Matches the logic in your app.py.
#     """
#     # Step 1: Hybrid retrieval
#     docs = hybrid_retrieve(
#         vector_store=db,
#         chunks=chunks,
#         query=query,
#         k=retrieval_k
#     )
    
#     # Step 2: Rerank (if rerank_k is specified)
#     if rerank_k is not None:
#         docs = rerank_documents(
#             query=query,
#             docs=docs,
#             top_k=rerank_k
#         )
    
#     return docs
# agents/retriever_agent.py - Updated
"""
Retriever Agent - Phase 5 Multi-Agent System
Version: 2.1 (Fixed Document handling)
"""

from typing import TypedDict, List, Optional, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import YOUR EXISTING retrieval functions from your app
try:
    from utils.retriver import retrieve_documents
    from utils.hybrid_retriver import hybrid_retrieve
    from utils.reranker import rerank_documents
except ImportError as e:
    print(f"⚠️ Error importing retrieval functions: {e}")
    raise


class AgentState(TypedDict):
    """State maintained across all agents in the LangGraph workflow"""
    query: str
    task: str
    plan: List[str]
    db: Any
    chunks: List[Any]
    retrieved_docs: Optional[List[Any]]
    research_output: Optional[str]
    final_answer: Optional[str]


def retriever_agent(state: AgentState) -> Dict:
    """
    Retriever Agent: Retrieves relevant documents using existing RAG pipeline.
    """
    
    query = state["query"]
    task = state["task"]
    plan = state.get("plan", [])
    
    # Get the vector database and chunks from state
    db = state.get("db")
    chunks = state.get("chunks")
    
    if db is None:
        print("❌ Error: No vector database found in state")
        return {
            "query": query,
            "task": task,
            "plan": plan,
            "db": db,
            "chunks": chunks,
            "retrieved_docs": [],
            "research_output": None,
            "final_answer": None
        }
    
    print(f"🔍 Retriever Agent: Processing task: {task}")
    print(f"   Query: {query}")
    
    # Determine retrieval strategy based on task
    try:
        if task == "summary":
            # For summarization, use all chunks
            retrieved_docs = chunks
            print(f"   📄 Using all {len(chunks)} chunks for summarization")
            
        elif task == "question_answering":
            retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=20, rerank_k=3)
            
        elif task == "research_gap":
            retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=20, rerank_k=None)
            
        elif task == "comparison":
            retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=30, rerank_k=15)
            
        elif task == "literature_review":
            retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=40, rerank_k=20)
            
        elif task == "citation":
            retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=25, rerank_k=12)
            
        else:
            retrieved_docs = _retrieve_with_hybrid(db, chunks, query, retrieval_k=20, rerank_k=3)
            
        print(f"   ✅ Retrieved {len(retrieved_docs)} documents")
        
    except Exception as e:
        print(f"   ❌ Retrieval failed: {e}")
        retrieved_docs = []
    
    # Update state with retrieved documents
    return {
        "query": query,
        "task": task,
        "plan": plan,
        "db": db,
        "chunks": chunks,
        "retrieved_docs": retrieved_docs,
        "research_output": None,
        "final_answer": None
    }


def _retrieve_with_hybrid(db: Any, chunks: List[Any], query: str, retrieval_k: int = 20, rerank_k: int = None) -> List[Any]:
    """Retrieve documents using hybrid search and optional reranking."""
    # Step 1: Hybrid retrieval
    docs = hybrid_retrieve(
        vector_store=db,
        chunks=chunks,
        query=query,
        k=retrieval_k
    )
    
    # Step 2: Rerank (if rerank_k is specified)
    if rerank_k is not None:
        docs = rerank_documents(
            query=query,
            docs=docs,
            top_k=rerank_k
        )
    
    return docs
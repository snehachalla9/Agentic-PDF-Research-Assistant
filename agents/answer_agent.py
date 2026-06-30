"""
Answer Agent - Phase 5 Multi-Agent System
Version: 1.2 (Fixed prompt builder parameters)
Purpose: Generate the final user-facing answer using your existing prompt builders
"""

from typing import TypedDict, List, Optional, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your existing utilities
try:
    from utils.llm import generate_answer
    from utils.prompt import build_prompt
    from utils.summary_prompt import build_summary_prompt
    from utils.research_gap_prompt import build_research_gap_prompt
    from utils.comparison_prompt import build_comparison_prompt
    from utils.literature_review_prompt import build_literature_review_prompt
    from utils.citation_prompt import build_citation_prompt
except ImportError as e:
    print(f"⚠️ Error importing utilities: {e}")
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


# Map task to prompt builder - matches your app.py
PROMPT_BUILDERS = {
    "question_answering": build_prompt,
    "summary": build_summary_prompt,
    "research_gap": build_research_gap_prompt,
    "comparison": build_comparison_prompt,
    "literature_review": build_literature_review_prompt,
    "citation": build_citation_prompt
}


def answer_agent(state: AgentState) -> Dict:
    """
    Answer Agent: Generates the final answer using your existing prompt builders.
    """
    
    query = state["query"]
    task = state["task"]
    docs = state.get("retrieved_docs", [])
    research_output = state.get("research_output", "")
    db = state.get("db")
    chunks = state.get("chunks")
    
    print(f"💬 Answer Agent: Generating final answer for task: {task}")
    
    try:
        # Get the appropriate prompt builder
        prompt_builder = PROMPT_BUILDERS.get(task)
        
        if not prompt_builder:
            print(f"   ⚠️ No prompt builder found for task: {task}")
            final_answer = _generate_fallback_answer(query, research_output, docs)
        else:
            # Build context from retrieved documents
            context = _build_context(docs)
            
            # Extract sources for tasks that need them
            sources = None
            if task in ["comparison", "literature_review", "citation"]:
                sources = _extract_sources(docs)
            
            # Build the prompt - handle different parameter signatures
            try:
                # Try with all parameters
                prompt = prompt_builder(
                    query=query,
                    context=context,
                    history=[],
                    sources=sources if sources else None
                )
            except TypeError as e:
                # If 'sources' parameter is not accepted, try without it
                if "sources" in str(e):
                    print("   ⚠️ Prompt builder doesn't accept 'sources', trying without...")
                    prompt = prompt_builder(
                        query=query,
                        context=context,
                        history=[]
                    )
                else:
                    # Try with just query and context
                    try:
                        prompt = prompt_builder(
                            query=query,
                            context=context
                        )
                    except:
                        # Final fallback: just use query
                        prompt = prompt_builder(query=query)
            
            # Generate answer using your existing LLM
            final_answer = generate_answer(prompt)
            
        print(f"   ✅ Answer generated ({len(final_answer)} characters)")
        
    except Exception as e:
        print(f"   ❌ Answer generation failed: {e}")
        # Try to use research output as fallback
        if research_output:
            final_answer = research_output
        else:
            final_answer = f"Error generating answer: {str(e)}"
    
    return {
        "query": query,
        "task": task,
        "plan": state.get("plan", []),
        "db": db,
        "chunks": chunks,
        "retrieved_docs": docs,
        "research_output": research_output,
        "final_answer": final_answer
    }


# --------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------

def _build_context(docs: List[Any]) -> str:
    """
    Build context from retrieved documents.
    Handles both Document objects and dictionaries.
    """
    if not docs:
        return "No documents retrieved."
    
    context_parts = []
    for doc in docs:
        # Handle Document objects (LangChain)
        if hasattr(doc, 'page_content'):
            content = doc.page_content
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
        # Handle dictionaries
        elif isinstance(doc, dict):
            content = doc.get("page_content", doc.get("content", doc.get("text", "")))
            metadata = doc.get("metadata", {})
        else:
            content = str(doc)
            metadata = {}
        
        # Format with metadata
        source = metadata.get("source", "Unknown")
        title = metadata.get("title", "")
        author = metadata.get("author", "")
        doi = metadata.get("doi", "")
        
        formatted_doc = f"""
Source: {source}
Title: {title}
Author: {author}
DOI: {doi}
{content}
"""
        context_parts.append(formatted_doc)
    
    return "\n\n".join(context_parts)


def _extract_sources(docs: List[Any]) -> List[str]:
    """Extract unique sources from documents"""
    sources = []
    for doc in docs:
        # Handle Document objects
        if hasattr(doc, 'metadata'):
            source = doc.metadata.get("source", "")
        elif isinstance(doc, dict):
            source = doc.get("metadata", {}).get("source", "")
        else:
            source = ""
        
        if source and source not in sources:
            sources.append(source)
    
    return sources


def _generate_fallback_answer(query: str, research_output: str, docs: List[Any]) -> str:
    """Generate fallback answer when prompt builder fails"""
    if research_output:
        return research_output
    
    if docs:
        context = _build_context(docs)
        prompt = f"""
Based on the following documents, answer this question:

Question: {query}

Documents:
{context}

Provide a clear and comprehensive answer.
"""
        try:
            return generate_answer(prompt)
        except:
            return f"Found {len(docs)} documents but couldn't generate answer."
    
    return "No relevant documents found to answer your question."


# --------------------------------------------------------------------
# Integration Helper - For use in app.py
# --------------------------------------------------------------------

def integrate_with_app(
    query: str,
    task: str,
    db: Any,
    chunks: List[Any],
    retrieved_docs: List[Any],
    research_output: str,
    history: List[Dict] = None
) -> str:
    """
    Helper to integrate with your Streamlit app.
    """
    state = {
        "query": query,
        "task": task,
        "plan": [],
        "db": db,
        "chunks": chunks,
        "retrieved_docs": retrieved_docs,
        "research_output": research_output,
        "final_answer": None
    }
    
    result = answer_agent(state)
    return result["final_answer"]
"""
Research Agent - Phase 5 Multi-Agent System
Version: 1.1 (Fixed Document handling)
Purpose: Process retrieved documents and generate research insights
"""

from typing import TypedDict, List, Optional, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your existing LLM setup
try:
    from utils.llm import generate_answer
except ImportError:
    print("⚠️ Warning: Could not import LLM. Please configure utils/llm.py")
    
    def generate_answer(prompt: str) -> str:
        """Placeholder - replace with your actual LLM"""
        return f"[Research Agent - LLM Not Configured]\n\nRequest: {prompt[:100]}..."


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


def research_agent(state: AgentState) -> Dict:
    """
    Research Agent: Generates research output based on task and retrieved documents.
    """
    
    query = state["query"]
    task = state["task"]
    docs = state.get("retrieved_docs", [])
    plan = state.get("plan", [])
    db = state.get("db")
    chunks = state.get("chunks")
    
    print(f"📚 Research Agent: Processing task: {task}")
    print(f"   Working with {len(docs)} documents")
    
    if not docs:
        print("   ⚠️ No documents available for research")
        return {
            "query": query,
            "task": task,
            "plan": plan,
            "db": db,
            "chunks": chunks,
            "retrieved_docs": docs,
            "research_output": "No documents were retrieved.",
            "final_answer": None
        }
    
    # Generate research output based on task
    try:
        if task == "question_answering":
            research_output = _research_qa(query, docs)
            
        elif task == "summary":
            research_output = _research_summary(query, docs)
            
        elif task == "research_gap":
            research_output = _research_gap(query, docs)
            
        elif task == "comparison":
            research_output = _research_comparison(query, docs)
            
        elif task == "literature_review":
            research_output = _research_literature_review(query, docs)
            
        elif task == "citation":
            research_output = _research_citation(query, docs)
            
        else:
            research_output = _research_default(query, docs)
            
        print(f"   ✅ Research output generated ({len(research_output)} characters)")
        
    except Exception as e:
        print(f"   ❌ Research generation failed: {e}")
        research_output = f"Error generating research output: {str(e)}"
    
    return {
        "query": query,
        "task": task,
        "plan": plan,
        "db": db,
        "chunks": chunks,
        "retrieved_docs": docs,
        "research_output": research_output,
        "final_answer": None
    }


# --------------------------------------------------------------------
# Task-Specific Research Functions
# --------------------------------------------------------------------

def _research_qa(query: str, docs: List[Any]) -> str:
    """Generate research analysis for QA"""
    context = _prepare_context(docs)
    
    prompt = f"""
You are a research assistant analyzing academic papers.

Question: {query}

Documents:
{context}

Analyze these documents and prepare a research summary:
1. Key findings from the documents
2. Supporting evidence with citations [1], [2], etc.
3. Any conflicting information
4. Gaps in the evidence

Research Summary:
"""
    return generate_answer(prompt)


def _research_summary(query: str, docs: List[Any]) -> str:
    """Generate research summary"""
    context = _prepare_context(docs)
    
    prompt = f"""
You are a research assistant summarizing academic papers.

Documents:
{context}

Create a structured research summary:
1. Background & Context
2. Methodology
3. Key Findings
4. Contributions
5. Conclusions & Limitations

Research Summary:
"""
    return generate_answer(prompt)


def _research_gap(query: str, docs: List[Any]) -> str:
    """Generate research gap analysis"""
    context = _prepare_context(docs)
    
    prompt = f"""
You are a research assistant analyzing research gaps.

Documents:
{context}

Identify and analyze research gaps:
1. Current State of Research
2. Identified Gaps and Limitations
3. Methodological Challenges
4. Future Research Directions
5. Priority Gaps

Research Gap Analysis:
"""
    return generate_answer(prompt)


def _research_comparison(query: str, docs: List[Any]) -> str:
    """Generate comparison analysis"""
    context = _prepare_context(docs)
    
    prompt = f"""
You are a research assistant comparing papers.

Request: {query}

Documents:
{context}

Create a detailed comparison:
1. Papers Being Compared
2. Methodology Comparison
3. Results Comparison
4. Strengths & Weaknesses
5. Recommendations

Comparison Analysis:
"""
    return generate_answer(prompt)


def _research_literature_review(query: str, docs: List[Any]) -> str:
    """Generate literature review"""
    context = _prepare_context(docs)
    
    prompt = f"""
You are a research assistant writing a literature review.

Topic: {query}

Documents:
{context}

Write a comprehensive literature review:
1. Introduction
2. Thematic Organization
3. Key Contributions
4. Research Gaps
5. Future Directions
6. Conclusion

Literature Review:
"""
    return generate_answer(prompt)


def _research_citation(query: str, docs: List[Any]) -> str:
    """Extract citation information"""
    citations = []
    for i, doc in enumerate(docs, 1):
        # Handle Document objects
        if hasattr(doc, 'metadata'):
            metadata = doc.metadata
        elif isinstance(doc, dict):
            metadata = doc.get("metadata", {})
        else:
            metadata = {}
        
        source = metadata.get("source", "Unknown")
        title = metadata.get("title", f"Paper {i}")
        author = metadata.get("author", "Unknown Author")
        citations.append(f"[{i}] {author}. \"{title}.\" {source}")
    
    return "\n\n".join(citations) if citations else "No citation information available."


def _research_default(query: str, docs: List[Any]) -> str:
    """Default research output"""
    context = _prepare_context(docs)
    
    prompt = f"""
Request: {query}

Documents:
{context}

Provide a comprehensive research analysis.
"""
    return generate_answer(prompt)


# --------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------

def _prepare_context(docs: List[Any], max_chars: int = 4000) -> str:
    """
    Prepare document context for LLM prompts.
    Handles both Document objects and dictionaries.
    """
    context_parts = []
    char_count = 0
    
    for i, doc in enumerate(docs, 1):
        # Handle Document objects (LangChain)
        if hasattr(doc, 'page_content'):
            content = doc.page_content
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
        # Handle dictionaries
        elif isinstance(doc, dict):
            content = doc.get("page_content", doc.get("content", doc.get("text", "")))
            metadata = doc.get("metadata", {})
        else:
            # Fallback
            content = str(doc)
            metadata = {}
        
        # Get source from metadata
        source = metadata.get("source", f"Document {i}")
        
        entry = f"[{i}] Source: {source}\n{content}\n"
        
        if char_count + len(entry) > max_chars:
            remaining = max_chars - char_count
            if remaining > 100:
                entry = f"[{i}] Source: {source}\n{content[:remaining-50]}...\n"
                context_parts.append(entry)
            break
        
        context_parts.append(entry)
        char_count += len(entry)
    
    return "\n".join(context_parts) if context_parts else "No document context available."
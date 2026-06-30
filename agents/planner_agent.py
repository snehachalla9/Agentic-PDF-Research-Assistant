"""
Planner Agent - Phase 5 Multi-Agent System
Version: 1.0 (Rule-based)
Purpose: Understand user intent and route to appropriate workflow
"""

from typing import TypedDict, List, Optional, Any
import re


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


def planner_agent(state: AgentState) -> dict:
    """
    Planner Agent: Analyzes user query and determines the appropriate task type.
    
    Task mapping:
        - "Ask Questions" → question_answering
        - "Summarize Paper" → summary
        - "Research Gaps" → research_gap
        - "Compare Papers" → comparison
        - "Literature Review" → literature_review
        - "Generate Citations" → citation
    """
    
    query = state["query"].strip()
    query_lower = query.lower()
    
    # Get existing state values
    db = state.get("db")
    chunks = state.get("chunks")
    
    # --------------------------------------------------------------------
    # Task 1: Question Answering
    # --------------------------------------------------------------------
    qa_keywords = [
        r'\bwhat\b', r'\bwho\b', r'\bwhere\b', r'\bwhen\b',
        r'\bwhy\b', r'\bhow\b', r'\bexplain\b', r'\bdefine\b',
        r'\bdoes\b', r'\bis\b', r'\bare\b', r'\bcan\b',
        r'\bwould\b', r'\bcould\b', r'\bshould\b'
    ]
    
    if any(re.search(pattern, query_lower) for pattern in qa_keywords):
        return {
            "query": query,
            "task": "question_answering",
            "plan": [
                "Analyze question to identify key concepts",
                "Retrieve relevant document chunks",
                "Rerank retrieved chunks for relevance",
                "Generate comprehensive answer with citations",
                "Validate answer against source material"
            ],
            "db": db,
            "chunks": chunks,
            "retrieved_docs": None,
            "research_output": None,
            "final_answer": None
        }
    
    # --------------------------------------------------------------------
    # Task 2: Summarization
    # --------------------------------------------------------------------
    summary_keywords = [
        r'\bsummary\b', r'\bsummarize\b', r'\bsummarise\b',
        r'\bsummarization\b', r'\boverview\b'
    ]
    
    if any(re.search(pattern, query_lower) for pattern in summary_keywords):
        return {
            "query": query,
            "task": "summary",
            "plan": [
                "Read entire document comprehensively",
                "Extract key contributions and findings",
                "Identify methodology and results",
                "Generate structured summary",
                "Add citations to original work"
            ],
            "db": db,
            "chunks": chunks,
            "retrieved_docs": None,
            "research_output": None,
            "final_answer": None
        }
    
    # --------------------------------------------------------------------
    # Task 3: Research Gap Analysis
    # --------------------------------------------------------------------
    gap_keywords = [
        r'research gap', r'future work', r'future direction',
        r'limitations', r'open question', r'remaining challenge',
        r'what is missing', r'gaps', r'gap analysis'
    ]
    
    if any(re.search(pattern, query_lower) for pattern in gap_keywords):
        return {
            "query": query,
            "task": "research_gap",
            "plan": [
                "Retrieve discussion and conclusion sections",
                "Extract mentioned limitations explicitly",
                "Identify unaddressed research questions",
                "Analyze potential future research directions",
                "Synthesize gaps across multiple papers",
                "Generate comprehensive research gap analysis"
            ],
            "db": db,
            "chunks": chunks,
            "retrieved_docs": None,
            "research_output": None,
            "final_answer": None
        }
    
    # --------------------------------------------------------------------
    # Task 4: Paper Comparison
    # --------------------------------------------------------------------
    comparison_keywords = [
        r'\bcompare\b', r'\bvs\b', r'\bversus\b',
        r'compare and contrast', r'difference between',
        r'similarities between', r'comparison'
    ]
    
    if any(re.search(pattern, query_lower) for pattern in comparison_keywords):
        return {
            "query": query,
            "task": "comparison",
            "plan": [
                "Identify papers to compare from query",
                "Retrieve full text of Paper A",
                "Retrieve full text of Paper B",
                "Extract methodology from both papers",
                "Compare datasets and evaluation metrics",
                "Compare results and performance",
                "Compare strengths and weaknesses",
                "Generate side-by-side comparison table",
                "Provide final recommendation"
            ],
            "db": db,
            "chunks": chunks,
            "retrieved_docs": None,
            "research_output": None,
            "final_answer": None
        }
    
    # --------------------------------------------------------------------
    # Task 5: Literature Review
    # --------------------------------------------------------------------
    review_keywords = [
        r'literature review', r'\bsurvey\b', r'comprehensive review',
        r'systematic review', r'state of the art', r'related work',
        r'review of', r'literature survey'
    ]
    
    if any(re.search(pattern, query_lower) for pattern in review_keywords):
        return {
            "query": query,
            "task": "literature_review",
            "plan": [
                "Identify relevant papers in domain",
                "Retrieve all relevant papers",
                "Extract key contributions from each paper",
                "Organize papers chronologically",
                "Group papers by themes/approaches",
                "Identify research trends over time",
                "Generate comprehensive literature review",
                "Include taxonomy of methods if applicable",
                "Add comprehensive reference list"
            ],
            "db": db,
            "chunks": chunks,
            "retrieved_docs": None,
            "research_output": None,
            "final_answer": None
        }
    
    # --------------------------------------------------------------------
    # Task 6: Citation Generation
    # --------------------------------------------------------------------
    citation_keywords = [
        r'\bcitation\b', r'\bcite\b', r'\bieee\b',
        r'\bapa\b', r'\bmla\b', r'\bbibtex\b',
        r'\breference\b', r'\bbibliography\b',
        r'generate citation', r'format citation'
    ]
    
    if any(re.search(pattern, query_lower) for pattern in citation_keywords):
        # Detect citation format requested
        citation_format = "ieee"
        if "apa" in query_lower:
            citation_format = "apa"
        elif "mla" in query_lower:
            citation_format = "mla"
        elif "bibtex" in query_lower:
            citation_format = "bibtex"
            
        return {
            "query": query,
            "task": "citation",
            "plan": [
                "Extract paper metadata from query",
                "Retrieve full paper metadata",
                "Extract title, authors, journal, year, volume, pages",
                f"Format citation in {citation_format.upper()} style",
                "Validate citation format",
                "Generate formatted citation"
            ],
            "db": db,
            "chunks": chunks,
            "retrieved_docs": None,
            "research_output": None,
            "final_answer": None
        }
    
    # --------------------------------------------------------------------
    # Default: Question Answering
    # --------------------------------------------------------------------
    return {
        "query": query,
        "task": "question_answering",
        "plan": [
            "Analyze user question",
            "Retrieve relevant document chunks",
            "Rerank chunks for relevance",
            "Generate contextual answer",
            "Add source citations",
            "Provide follow-up suggestions if relevant"
        ],
        "db": db,
        "chunks": chunks,
        "retrieved_docs": None,
        "research_output": None,
        "final_answer": None
    }


def extract_comparison_papers(query: str) -> List[str]:
    """
    Extract paper names from comparison query.
    Example: "Compare paper1 and paper2" → ["paper1", "paper2"]
    """
    # Remove comparison keywords
    clean = re.sub(r'compare|vs|versus|comparison', '', query, flags=re.IGNORECASE)
    
    # Split by "and" or ","
    parts = re.split(r'\band\b|,', clean)
    
    papers = []
    for part in parts:
        paper = part.strip()
        if paper and len(paper) > 2:  # Avoid empty or very short matches
            papers.append(paper)
    
    return papers if len(papers) >= 2 else []
def build_research_gap_prompt(query=None, context=None, history=None, sources=None):
    """Build a prompt for identifying research gaps."""
    query_text = query if query else "Identify research gaps and future work"
    
    prompt = f"""
You are a research assistant identifying gaps in the literature.

Using the context below, identify:
1. **Research Gaps**: What questions remain unanswered?
2. **Limitations**: What are the limitations of current approaches?
3. **Future Work**: What directions should future research take?
4. **Improvements**: What could be done better?

User Question: {query_text}

Context:
{context}

Research Gaps Analysis:
"""
    return prompt
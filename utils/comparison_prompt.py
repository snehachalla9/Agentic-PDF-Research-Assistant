def build_comparison_prompt(query=None, context=None, history=None, sources=None):
    """Build a prompt for comparing papers."""
    sources_text = "\n".join([f"• {source}" for source in sources]) if sources else "Multiple papers"
    query_text = query if query else "Compare these papers"
    
    prompt = f"""
You are a research assistant comparing multiple academic papers.

Papers being compared:
{sources_text}

Relevant excerpts:
{context}

User Question: {query_text}

Please provide a thorough comparison that:
1. **Key Similarities**: What do these papers have in common?
2. **Key Differences**: How do they differ in approach or findings?
3. **Contradictory Findings**: Are there any conflicts between papers?
4. **Methodological Differences**: How do their methodologies compare?
5. **Relative Strengths**: What does each paper do well?

Comparison:
"""
    return prompt
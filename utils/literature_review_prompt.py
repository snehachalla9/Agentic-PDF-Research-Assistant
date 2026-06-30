def build_literature_review_prompt(query=None, context=None, history=None, sources=None):
    """Build a prompt for literature review synthesis."""
    sources_text = "\n".join([f"• {source}" for source in sources]) if sources else "Multiple papers"
    query_text = query if query else "Synthesize the literature"
    
    prompt = f"""
You are a research assistant conducting a literature review.

Papers being reviewed:
{sources_text}

Relevant excerpts:
{context}

User Question: {query_text}

Please provide a comprehensive literature review that:
1. **Main Themes**: What are the dominant themes across all papers?
2. **Methodological Patterns**: What methods are commonly used?
3. **Key Findings**: What are the consensus findings?
4. **Areas of Disagreement**: Where do papers conflict?
5. **Gaps**: What is missing from the literature?
6. **Future Directions**: What should be studied next?

Literature Review:
"""
    return prompt
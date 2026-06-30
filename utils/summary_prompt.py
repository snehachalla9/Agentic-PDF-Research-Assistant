def build_summary_prompt(query=None, context=None, history=None, sources=None):
    """Build a prompt for paper summarization."""
    # query is optional for summary
    prompt = f"""
You are a research assistant summarizing an academic paper.

Using the complete text below, provide a comprehensive summary that includes:
1. **Research Question**: What problem does this paper address?
2. **Methodology**: What approach did the authors take?
3. **Key Findings**: What are the main results?
4. **Contributions**: What is novel about this work?
5. **Limitations**: What are the limitations of this study?

Paper Content:
{context}

Summary:
"""
    return prompt
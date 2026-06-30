def build_citation_prompt(query=None, context=None, history=None, sources=None):
    """Build a prompt for generating IEEE citations."""
    sources_text = "\n".join([f"• {source}" for source in sources]) if sources else "Papers to cite"
    query_text = query if query else "Generate IEEE citations"
    
    prompt = f"""
You are a research assistant helping with academic citations.

Papers to cite:
{sources_text}

Relevant excerpts:
{context}

User Request: {query_text}

Please generate IEEE-formatted citations. Follow these formats:

**Conference Paper:**
[1] Author Initials. Author Surname, "Title of Paper," in *Conference Name*, Location, Year, pp. Page Numbers, doi: DOI.

**Journal Article:**
[2] Author Initials. Author Surname, "Title of Article," *Journal Name*, vol. Volume, no. Issue, pp. Page Numbers, Month Year, doi: DOI.

**Book:**
[3] Author Initials. Author Surname, *Book Title*. Publisher, Year, pp. Page Numbers.

Generate accurate citations for all papers mentioned in the context. Use consistent numbering throughout.

Citations:
"""
    return prompt
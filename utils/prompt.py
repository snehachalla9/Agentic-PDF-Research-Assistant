def build_prompt(
        query,
        context,
        history
):
    prompt=f"""
yor are a helpful AI assistant.
Use the provided context  answer the question.
If the answer can be inferred from the context,
provide the answer.
If the answer is not available in the context,
say "I couldn't  find that information in the document."
chat history:
{history}
context:
{context}
question:
{query}
Answer:
"""
    return prompt

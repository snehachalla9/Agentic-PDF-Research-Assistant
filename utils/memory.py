def get_chat_history(messages):
    """
    convert chat messages into formatted history
    """
    history=""
    for msg in messages:
        history+=f"""
        user:{msg['question']}
        assistant:{msg['answer']}
"""
        return history
    

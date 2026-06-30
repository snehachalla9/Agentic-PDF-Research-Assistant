from database.supabase import supabase


# =====================================
# Conversation Functions
# =====================================

def create_conversation(user_id, title):
    """
    Create a new conversation.
    """

    response = (
        supabase.table("conversations")
        .insert(
            {
                "user_id": user_id,
                "title": title
            }
        )
        .execute()
    )

    return response.data


def get_conversations(user_id):
    """
    Get all conversations for a user.
    """

    response = (
        supabase.table("conversations")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


# =====================================
# Chat Functions
# =====================================

def save_chat(conversation_id,
              user_id,
              question,
              answer,
              task):

    response = (
        supabase.table("chat_history")
        .insert(
            {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "question": question,
                "answer": answer,
                "task": task
            }
        )
        .execute()
    )

    return response.data


def get_chat_history(conversation_id):

    response = (
        supabase.table("chat_history")
        .select("*")
        .eq("conversation_id", conversation_id)
        .order("created_at")
        .execute()
    )

    return response.data
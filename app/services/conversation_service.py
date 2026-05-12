conversation_store = {}

MAX_TURNS = 8


def save_conversation(session_id, query):

    if session_id not in conversation_store:

        conversation_store[session_id] = []

    conversation_store[session_id].append(query)

    # KEEP ONLY LAST 8 TURNS
    conversation_store[session_id] = (
        conversation_store[session_id][-MAX_TURNS:]
    )


def get_conversation_context(session_id):

    return conversation_store.get(session_id, [])
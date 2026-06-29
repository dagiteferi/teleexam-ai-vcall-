from app.agents.state import AgentState


def test_agent_state_has_all_expected_fields():
    expected_fields = {
        "session_id",
        "telegram_id",
        "user_id",
        "transcript",
        "chat_history",
        "intent",
        "confidence",
        "key_entities",
        "search_results",
        "youtube_data",
        "rag_context",
        "user_profile",
        "ai_response",
        "error",
        "latency_ms",
    }

    assert set(AgentState.__annotations__.keys()) == expected_fields


def test_can_create_valid_agent_state():
    state: AgentState = {
        "session_id": "session-123",
        "telegram_id": 123456789,
        "user_id": 1,
        "transcript": "Explain binary trees",
        "chat_history": [],
        "intent": "question_answer",
        "confidence": 0.98,
        "key_entities": ["Binary Tree"],
        "search_results": "Search results",
        "youtube_data": {"video_id": "abc123"},
        "rag_context": "Relevant notes",
        "user_profile": {"level": "beginner"},
        "ai_response": "A binary tree is...",
        "error": None,
        "latency_ms": 250,
    }

    assert state["session_id"] == "session-123"
    assert state["intent"] == "question_answer"


def test_chat_history_accepts_list_of_dicts():
    state: AgentState = {
        "session_id": "session-123",
        "telegram_id": 123456789,
        "user_id": 1,
        "transcript": "Hello",
        "chat_history": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi!"},
        ],
        "intent": "greeting",
        "confidence": 1.0,
        "key_entities": [],
        "search_results": None,
        "youtube_data": None,
        "rag_context": None,
        "user_profile": None,
        "ai_response": None,
        "error": None,
        "latency_ms": None,
    }

    assert isinstance(state["chat_history"], list)
    assert all(isinstance(item, dict) for item in state["chat_history"])


def test_optional_fields_can_be_none():
    state: AgentState = {
        "session_id": "session-123",
        "telegram_id": 123456789,
        "user_id": 1,
        "transcript": "Hello",
        "chat_history": [],
        "intent": "greeting",
        "confidence": 1.0,
        "key_entities": [],
        "search_results": None,
        "youtube_data": None,
        "rag_context": None,
        "user_profile": None,
        "ai_response": None,
        "error": None,
        "latency_ms": None,
    }

    assert state["search_results"] is None
    assert state["youtube_data"] is None
    assert state["rag_context"] is None
    assert state["user_profile"] is None
    assert state["ai_response"] is None
    assert state["error"] is None
    assert state["latency_ms"] is None
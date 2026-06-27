from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    session_id: str
    telegram_id: int
    user_id: int
    transcript: str
    chat_history: List[dict]
    intent: str
    confidence: float
    key_entities: List[str]
    search_results: Optional[str]
    youtube_data: Optional[dict]
    rag_context: Optional[str]
    user_profile: Optional[dict]
    ai_response: Optional[str]
    error: Optional[str]
    latency_ms: Optional[int]
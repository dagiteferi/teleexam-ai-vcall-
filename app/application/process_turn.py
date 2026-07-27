import json
import time
from datetime import UTC, datetime
from uuid import uuid4

from app.agents.deps import AgentDependencies
from app.agents.graph import CALL_GRAPH
from app.agents.state import AgentState
from app.domain.models import Turn


async def process_turn(
    session_id: str,
    transcript: str,
    telegram_id: int,
    user_id: int,
    deps: AgentDependencies,
) -> AgentState:
    """
    Process one student utterance through the complete LangGraph pipeline.
    """

    # Start latency timer
    start = time.monotonic()

    # Redis key for conversation state
    cache_key = f"vcall:session:{session_id}"

    # Try loading previous conversation state
    cached_state = await deps.cache.get(cache_key)

    if cached_state:
        state: AgentState = json.loads(cached_state)
    else:
        state: AgentState = {
            "session_id": session_id,
            "telegram_id": telegram_id,
            "user_id": user_id,
            "transcript": "",
            "chat_history": [],
            "intent": "",
            "confidence": 0.0,
            "key_entities": [],
            "search_results": None,
            "youtube_data": None,
            "rag_context": None,
            "user_profile": None,
            "ai_response": None,
            "error": None,
            "latency_ms": None,
        }

    # Update transcript with newest student message
    state["transcript"] = transcript

    # Run LangGraph
    result: AgentState = await CALL_GRAPH.ainvoke(
        state,
        config={
            "configurable": {
                "deps": deps,
            }
        },
    )

    # Measure latency
    result["latency_ms"] = int(
        (time.monotonic() - start) * 1000
    )

    # Save conversation turn
    turn = Turn(
        turn_id=str(uuid4()),
        session_id=session_id,
        transcript=transcript,
        intent=result["intent"],
        ai_response=result["ai_response"],
        latency_ms=result["latency_ms"],
        created_at=datetime.now(UTC),
    )

    await deps.call_repo.save_turn(turn)

    # Cache updated conversation state
    await deps.cache.set(
        key=cache_key,
        value=json.dumps(result),
        ttl_seconds=1800,
    )

    return result
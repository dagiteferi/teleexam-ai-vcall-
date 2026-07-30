import pytest

from app.agents.graph import CALL_GRAPH
from app.agents.deps import AgentDependencies
from app.agents.supervisor import IntentResult

from tests.fakes import (
    FakeLLMPort,
    FakeCachePort,
    FakeEmbeddingPort,
    FakeVectorSearchPort,
    FakeTTSPort,
)

pytestmark = pytest.mark.integration


class DummySTTPort:
    pass


class DummyWebSearchPort:
    async def search(self, query: str):
        return "Dummy search result"


class DummyVideoSearchPort:
    async def search(self, query: str):
        return []


class DummyMediaPort:
    pass


class DummyCallRepository:
    pass


class DummyProfileRepository:
    async def get_by_telegram_id(self, telegram_id: int):
        return None


class DummyCurriculumRepository:
    pass


@pytest.mark.asyncio
async def test_full_pipeline_exam_question():

    state = {
        "session_id": "test_session_001",
        "telegram_id": 123456789,
        "user_id": 1,
        "transcript": "What is the time complexity of binary search?",
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

    deps = AgentDependencies(
        llm=FakeLLMPort(
            IntentResult(
                intent="exam_question",
                confidence=0.95,
                key_entities=[
                    "binary search",
                    "time complexity",
                ],
            )
        ),
        stt=DummySTTPort(),
        tts=FakeTTSPort(),
        embeddings=FakeEmbeddingPort(),
        vector_search=FakeVectorSearchPort(),
        web_search=DummyWebSearchPort(),
        video_search=DummyVideoSearchPort(),
        cache=FakeCachePort(),
        media=DummyMediaPort(),
        call_repo=DummyCallRepository(),
        profile_repo=DummyProfileRepository(),
        curriculum_repo=DummyCurriculumRepository(),
    )

    result = await CALL_GRAPH.ainvoke(
        state,
        config={
            "configurable": {
                "deps": deps,
            }
        },
    )

    assert result["intent"] == "exam_question"
    assert result["rag_context"] is not None
    assert isinstance(result["rag_context"], str)

    assert result["ai_response"] is not None
    assert isinstance(result["ai_response"], str)

    assert len(result["chat_history"]) == 2

    assert result["error"] is None


@pytest.mark.asyncio
async def test_full_pipeline_general_tutor():

    state = {
        "session_id": "test_session_001",
        "telegram_id": 123456789,
        "user_id": 1,
        "transcript": "Hello, can you help me study?",
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

    deps = AgentDependencies(
        llm=FakeLLMPort(
            IntentResult(
                intent="general_tutor",
                confidence=0.95,
                key_entities=[],
            )
        ),
        stt=DummySTTPort(),
        tts=FakeTTSPort(),
        embeddings=FakeEmbeddingPort(),
        vector_search=FakeVectorSearchPort(),
        web_search=DummyWebSearchPort(),
        video_search=DummyVideoSearchPort(),
        cache=FakeCachePort(),
        media=DummyMediaPort(),
        call_repo=DummyCallRepository(),
        profile_repo=DummyProfileRepository(),
        curriculum_repo=DummyCurriculumRepository(),
    )

    result = await CALL_GRAPH.ainvoke(
        state,
        config={
            "configurable": {
                "deps": deps,
            }
        },
    )

    assert result["intent"] == "general_tutor"
    assert result["rag_context"] is None

    assert result["ai_response"] is not None
    assert isinstance(result["ai_response"], str)

    assert len(result["chat_history"]) == 2

    assert result["error"] is None
import pytest

from app.agents.curriculum_agent import curriculum_agent_node
from app.agents.synthesizer import synthesizer_node
from app.agents.deps import AgentDependencies

from tests.fakes import (
    FakeLLMPort,
    FakeCachePort,
    FakeEmbeddingPort,
    FakeVectorSearchPort,
    FakeTTSPort,
    FakeMediaSessionPort,
)


def create_fake_deps():

    return AgentDependencies(
        llm=FakeLLMPort(),
        stt=None,
        tts=FakeTTSPort(),
        embeddings=FakeEmbeddingPort(),
        vector_search=FakeVectorSearchPort(),
        web_search=None,
        video_search=None,
        cache=FakeCachePort(),
        media=FakeMediaSessionPort(),
        call_repo=None,
        profile_repo=None,
        curriculum_repo=None,
    )


def create_test_config():

    deps = create_fake_deps()

    return {
        "configurable": {
            "deps": deps
        }
    }


@pytest.mark.asyncio
async def test_curriculum_agent_sets_rag_context():

    state = {
        "transcript": "Explain data structures"
    }

    result = await curriculum_agent_node(
        state,
        create_test_config(),
    )

    assert "rag_context" in result
    assert isinstance(
        result["rag_context"],
        str,
    )


@pytest.mark.asyncio
async def test_synthesizer_with_rag_context_sets_response():

    state = {
        "transcript": "Explain arrays",
        "rag_context": "Arrays store elements in contiguous memory",
        "chat_history": [],
    }

    result = await synthesizer_node(
        state,
        create_test_config(),
    )

    assert "ai_response" in result
    assert isinstance(
        result["ai_response"],
        str,
    )


@pytest.mark.asyncio
async def test_synthesizer_with_search_results_sets_response():

    state = {
        "transcript": "Latest AI trends",
        "search_results": "AI research article",
        "chat_history": [],
    }

    result = await synthesizer_node(
        state,
        create_test_config(),
    )

    assert "ai_response" in result
    assert isinstance(
        result["ai_response"],
        str,
    )


@pytest.mark.asyncio
async def test_synthesizer_grows_chat_history():

    state = {
        "transcript": "What is Python?",
        "chat_history": [],
    }

    result = await synthesizer_node(
        state,
        create_test_config(),
    )

    assert len(result["chat_history"]) == 2
import pytest

from app.agents.supervisor import supervisor_node
from app.agents.deps import AgentDependencies

from tests.fakes import (
    FakeLLMPort,
    FakeCachePort,
    FakeEmbeddingPort,
    FakeVectorSearchPort,
    FakeMediaSessionPort,
)


def create_fake_deps():

    return AgentDependencies(
        llm=FakeLLMPort(),
        stt=None,
        tts=None,
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
async def test_supervisor_sets_valid_intent():

    state = {
        "transcript": "Explain binary search"
    }

    result = await supervisor_node(
        state,
        create_test_config(),
    )

    assert "intent" in result
    assert result["intent"] is not None


@pytest.mark.asyncio
async def test_supervisor_sets_confidence_float():

    state = {
        "transcript": "What is recursion?"
    }

    result = await supervisor_node(
        state,
        create_test_config(),
    )

    assert isinstance(
        result["confidence"],
        float,
    )


@pytest.mark.asyncio
async def test_supervisor_stores_result_in_cache():

    state = {
        "transcript": "Explain linked lists"
    }

    deps = create_fake_deps()

    config = {
        "configurable": {
            "deps": deps
        }
    }

    await supervisor_node(
        state,
        config,
    )

    keys = list(deps.cache.store.keys())

    assert any(
        key.startswith("vcall:intent:")
        for key in keys
    )


@pytest.mark.asyncio
async def test_supervisor_uses_cache_second_time():

    state = {
        "transcript": "Explain linked lists"
    }

    deps = create_fake_deps()

    config = {
        "configurable": {
            "deps": deps
        }
    }

    first_result = await supervisor_node(
        state,
        config,
    )

    second_result = await supervisor_node(
        state,
        config,
    )

    assert second_result["intent"] == first_result["intent"]
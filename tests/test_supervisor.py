import pytest

from app.agents.supervisor import supervisor_node
from app.agents.deps import AgentDependencies

from tests.fakes import (
    FakeLLMPort,
    FakeCachePort,
    FakeEmbeddingPort,
    FakeVectorSearchPort,
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
        call_repo=None,
        profile_repo=None,
        curriculum_repo=None,
    )


@pytest.mark.asyncio
async def test_supervisor_sets_valid_intent():

    state = {
        "transcript": "Explain binary search"
    }

    deps = create_fake_deps()

    result = await supervisor_node(
        state,
        deps,
    )

    assert result["intent"] in [
        "concept_search",
        "youtube_find",
        "youtube_summary",
        "exam_question",
        "memory_query",
        "general_tutor",
        "unknown",
    ]


@pytest.mark.asyncio
async def test_supervisor_sets_confidence_float():

    state = {
        "transcript": "What is recursion?"
    }

    deps = create_fake_deps()

    result = await supervisor_node(
        state,
        deps,
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

    await supervisor_node(
        state,
        deps,
    )

    assert len(deps.cache.store) == 1


@pytest.mark.asyncio
async def test_supervisor_uses_cache_second_time():

    state = {
        "transcript": "Explain linked lists"
    }

    deps = create_fake_deps()

    first_result = await supervisor_node(
        state.copy(),
        deps,
    )

    second_result = await supervisor_node(
        state.copy(),
        deps,
    )

    assert first_result["intent"] == second_result["intent"]
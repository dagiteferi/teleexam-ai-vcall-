import json

from langchain_core.runnables import RunnableConfig

from app.agents.deps import AgentDependencies
from app.agents.state import AgentState
from app.core.utils import stable_hash


async def youtube_find_node(
    state: AgentState,
    config: RunnableConfig,
) -> AgentState:
    """
    Finds a YouTube video related to the student's request.
    Results are cached for 60 minutes.
    """

    deps: AgentDependencies = config["configurable"]["deps"]

    cache_key = f"vcall:yt:{stable_hash(state['transcript'])}"

    cached = await deps.cache.get(cache_key)

    if cached:
        state["youtube_data"] = json.loads(cached)
        return state

    result = await deps.video_search.find(
        state["transcript"]
    )

    await deps.cache.set(
        cache_key,
        json.dumps(result),
        ttl_seconds=3600,
    )

    state["youtube_data"] = result

    return state


async def youtube_summarize_node(
    state: AgentState,
    config: RunnableConfig,
) -> AgentState:
    """
    Summarizes a YouTube video.
    Uses an existing video URL if available,
    otherwise searches for one first.
    """

    deps: AgentDependencies = config["configurable"]["deps"]

    youtube_data = state.get("youtube_data")

    if youtube_data and youtube_data.get("url"):
        video_url = youtube_data["url"]
    else:
        youtube_data = await deps.video_search.find(
            state["transcript"]
        )

        state["youtube_data"] = youtube_data

        video_url = youtube_data["url"]

    summary = await deps.video_search.summarize(
        video_url
    )

    state["youtube_data"]["summary"] = summary

    return state
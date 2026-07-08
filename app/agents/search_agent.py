from app.agents.deps import AgentDependencies
from app.agents.state import AgentState
from app.core.utils import stable_hash


async def search_agent_node(
    state: AgentState,
    deps: AgentDependencies,
) -> AgentState:
    """
    Handles concept search requests.

    Checks Redis cache first. If no cached result exists,
    performs a web search, caches the result for 10 minutes,
    and stores it in the shared AgentState.
    """

    # Create a stable cache key
    cache_key = f"vcall:search:{stable_hash(state['transcript'])}"

    # Check cache first
    cached = await deps.cache.get(cache_key)

    if cached:
        state["search_results"] = cached
        return state

    # Perform web search
    result = await deps.web_search.search(
        state["transcript"]
    )

    # Cache the result for 10 minutes (600 seconds)
    await deps.cache.set(
        cache_key,
        result,
        ttl_seconds=600,
    )

    # Save the search result into the shared state
    state["search_results"] = result

    return state
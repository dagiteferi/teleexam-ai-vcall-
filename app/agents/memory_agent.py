import json

from app.agents.deps import AgentDependencies
from app.agents.state import AgentState


async def memory_agent_node(
    state: AgentState,
    deps: AgentDependencies,
) -> AgentState:
    """
    Loads the learner profile.

    Checks Redis first.
    If not cached, loads from the profile repository,
    caches it for 2 minutes, and stores it in AgentState.
    """

    # Build cache key
    cache_key = f"vcall:profile:{state['telegram_id']}"

    # Check Redis cache
    cached = await deps.cache.get(cache_key)

    if cached:
        state["user_profile"] = json.loads(cached)
        return state

    # Load profile from repository
    profile = await deps.profile_repo.get_by_telegram_id(
        state["telegram_id"]
    )

    if profile is not None:
        profile_dict = profile.model_dump()

        await deps.cache.set(
            cache_key,
            json.dumps(profile_dict),
            ttl_seconds=120,
        )

        state["user_profile"] = profile_dict
    else:
        state["user_profile"] = None

    return state
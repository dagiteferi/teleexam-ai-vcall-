from app.agents.deps import AgentDependencies


async def end_call_session(
    session_id: str,
    deps: AgentDependencies,
) -> None:
    # Get the session before updating it
    session = await deps.call_repo.get_by_id(session_id)

    if session is None:
        return

    # Mark the session as ended
    await deps.call_repo.update_status(
        session_id=session_id,
        status="ended",
    )

    # Remove the cached room
    await deps.cache.delete(
        f"vcall:room:{session.user_id}"
    )
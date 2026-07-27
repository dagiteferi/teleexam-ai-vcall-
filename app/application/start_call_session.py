from datetime import UTC, datetime
from uuid import uuid4

from app.agents.deps import AgentDependencies
from app.domain.models import CallSession


async def start_call_session(
    telegram_id: int,
    user_id: int,
    deps: AgentDependencies,
) -> CallSession:
    # Generate a unique session ID
    session_id = str(uuid4())

    # Create a unique LiveKit room name
    room_name = f"room_{session_id[:8]}"

    # Create the LiveKit room
    await deps.media.create_room(room_name)

    # Create the CallSession domain model
    session = CallSession(
        session_id=session_id,
        user_id=user_id,
        telegram_id=telegram_id,
        room_name=room_name,
        status="active",
        started_at=datetime.now(UTC),
    )

    # Save the session in PostgreSQL
    await deps.call_repo.save(session)

    # Cache the room name for 30 minutes
    await deps.cache.set(
        key=f"vcall:room:{user_id}",
        value=room_name,
        ttl_seconds=1800,
    )

    return session
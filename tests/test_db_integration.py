import pytest

from datetime import datetime, UTC
from uuid import uuid4

from app.adapters.outbound.db.postgres_call_repo import (
    PostgresCallRepository,
)
from app.adapters.outbound.db.postgres_curriculum_repo import (
    PostgresCurriculumRepository,
)
from app.adapters.outbound.db.postgres_vector_search import (
    PostgresVectorSearchAdapter,
)
from app.domain.models import (
    CallSession,
    CurriculumChunk,
)


pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_save_and_get_call_session(db_session):

    repo = PostgresCallRepository(db_session)

    session = CallSession(
        session_id=str(uuid4()),
        user_id=1,
        telegram_id=12345,
        room_name="room-test",
        status="active",
        started_at=datetime.now(UTC),
        ended_at=None,
    )

    await repo.save(session)

    result = await repo.get_by_id(
        session.session_id
    )

    assert result is not None
    assert result.session_id == session.session_id
    assert result.user_id == session.user_id
    assert result.status == "active"


@pytest.mark.asyncio
async def test_update_session_status(db_session):

    repo = PostgresCallRepository(db_session)

    session_id = str(uuid4())

    session = CallSession(
        session_id=session_id,
        user_id=2,
        telegram_id=222,
        room_name="room-ended",
        status="active",
        started_at=datetime.now(UTC),
        ended_at=None,
    )

    await repo.save(session)

    await repo.update_status(
        session_id,
        "ended",
    )

    result = await repo.get_by_id(session_id)

    assert result.status == "ended"
    assert result.ended_at is not None


@pytest.mark.asyncio
async def test_save_curriculum_chunk(db_session):

    repo = PostgresCurriculumRepository(
        db_session
    )

    chunk = CurriculumChunk(
        chunk_id=str(uuid4()),
        topic="Python",
        content="Python data structures",
        source="test.txt",
        embedding=[0.1] * 1024,
        created_at=datetime.now(UTC),
    )

    await repo.save_chunk(chunk)

    chunks = await repo.get_all_chunks()

    found = [
        c for c in chunks
        if c.chunk_id == chunk.chunk_id
    ]

    assert len(found) == 1
    assert found[0].embedding is not None


@pytest.mark.asyncio
async def test_vector_search_returns_strings(db_session):

    adapter = PostgresVectorSearchAdapter(
        db_session
    )

    results = await adapter.search(
        query_embedding=[0.1] * 1024,
        k=3,
    )

    assert isinstance(results, list)

    for item in results:
        assert isinstance(item, str)
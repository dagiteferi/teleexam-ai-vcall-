import pytest_asyncio

from app.core.database import async_session, engine


@pytest_asyncio.fixture
async def db_session():
    async with async_session() as session:
        yield session

    await engine.dispose()
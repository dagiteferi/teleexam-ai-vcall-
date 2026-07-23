import asyncio
import pytest

from app.adapters.outbound.cache.redis_adapter import (
    RedisAdapter,
)
from app.core.config import settings
from app.core.utils import stable_hash


pytestmark = pytest.mark.integration


@pytest.fixture
def redis_adapter():

    return RedisAdapter(
        host=settings.redis_host,
        port=settings.redis_port,
    )


@pytest.mark.asyncio
async def test_set_and_get(redis_adapter):

    await redis_adapter.set(
        "test:key",
        "hello",
        ttl_seconds=60,
    )

    result = await redis_adapter.get(
        "test:key"
    )

    assert result == "hello"


@pytest.mark.asyncio
async def test_delete_key(redis_adapter):

    await redis_adapter.set(
        "delete:key",
        "value",
    )

    await redis_adapter.delete(
        "delete:key"
    )

    result = await redis_adapter.get(
        "delete:key"
    )

    assert result is None


@pytest.mark.asyncio
async def test_key_expiration(redis_adapter):

    await redis_adapter.set(
        "expire:key",
        "value",
        ttl_seconds=1,
    )

    await asyncio.sleep(2)

    result = await redis_adapter.get(
        "expire:key"
    )

    assert result is None


@pytest.mark.asyncio
async def test_stable_hash_key_pattern(redis_adapter):

    key = f"vcall:intent:{stable_hash('test')}"

    await redis_adapter.set(
        key,
        "concept_search",
    )

    result = await redis_adapter.get(
        key
    )

    assert result == "concept_search"
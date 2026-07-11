import pytest

from app.adapters.outbound.embeddings.voyage_adapter import VoyageAdapter


@pytest.mark.asyncio
async def test_voyage_adapter_exists():

    adapter = VoyageAdapter.__new__(VoyageAdapter)

    assert isinstance(adapter, VoyageAdapter)
from typing import Optional, Protocol


class CachePort(Protocol):
    async def get(
        self,
        key: str,
    ) -> Optional[str]:
        ...

    async def set(
        self,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ) -> None:
        ...

    async def delete(
        self,
        key: str,
    ) -> None:
        ...
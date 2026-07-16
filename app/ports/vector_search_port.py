from typing import Protocol


class VectorSearchPort(Protocol):

    async def search(
        self,
        query_embedding: list[float],
        k: int = 5,
    ) -> list[str]:
        ...
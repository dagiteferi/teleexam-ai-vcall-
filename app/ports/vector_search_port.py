from typing import Protocol


class VectorSearchPort(Protocol):
    async def search(
        self,
        query_embedding: list[float],
        top_k: int,
    ) -> list[str]:
        ...
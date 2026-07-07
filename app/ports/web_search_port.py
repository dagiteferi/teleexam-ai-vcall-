from typing import Protocol


class WebSearchPort(Protocol):
    async def search(
        self,
        query: str,
    ) -> str:
        ...
from typing import Protocol


class EmbeddingPort(Protocol):
    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        ...

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        ...

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        ...
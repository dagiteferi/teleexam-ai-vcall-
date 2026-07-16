from voyageai import AsyncClient

from app.core.config import Settings
from app.ports.embedding_port import EmbeddingPort


class VoyageAdapter(EmbeddingPort):
    def __init__(self, settings: Settings):
        self.client = AsyncClient(
            api_key=settings.voyage_api_key
        )

    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        response = await self.client.embed(
            texts=texts,
            model="voyage-3",
        )

        return response.embeddings

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        embeddings = await self.embed([text])
        return embeddings[0]

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return await self.embed(texts)
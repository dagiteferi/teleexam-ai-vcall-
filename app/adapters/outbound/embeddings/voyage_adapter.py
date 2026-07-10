from voyageai import AsyncClient

from app.ports.embedding_port import EmbeddingPort
from app.core.config import Settings


class VoyageAdapter(EmbeddingPort):

    def __init__(self, settings: Settings):
        self.client = AsyncClient(
            api_key=settings.voyage_api_key
        )

    async def embed_text(self, text: str) -> list[float]:
        response = await self.client.embed(
            texts=[text],
            model="voyage-3"
        )

        return response.embeddings[0]


    async def embed_documents(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        response = await self.client.embed(
            texts=texts,
            model="voyage-3"
        )

        return response.embeddings
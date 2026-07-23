from tavily import AsyncTavilyClient

from app.core.config import Settings
from app.ports.web_search_port import WebSearchPort


class TavilyAdapter(WebSearchPort):
    def __init__(self, settings: Settings):
        self.client = AsyncTavilyClient(
            api_key=settings.tavily_api_key,
        )

    async def search(
        self,
        query: str,
    ) -> str:
        response = await self.client.search(
            query=query,
            max_results=3,
        )

        return response["results"][0]["content"]
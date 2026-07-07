from typing import Protocol


class VideoSearchPort(Protocol):
    async def find(
        self,
        query: str,
    ) -> dict:
        ...

    async def summarize(
        self,
        video_url: str,
    ) -> str:
        ...
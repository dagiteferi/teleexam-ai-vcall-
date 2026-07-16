from app.ports.video_search_port import VideoSearchPort


class YouTubeAdapter(VideoSearchPort):
    async def find(
        self,
        query: str,
    ) -> dict:
        return {}

    async def summarize(
        self,
        video_url: str,
    ) -> str:
        return ""
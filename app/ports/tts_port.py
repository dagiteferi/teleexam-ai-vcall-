from collections.abc import AsyncIterator
from typing import Protocol


class TTSPort(Protocol):
    async def speak_stream(
        self,
        text_stream: AsyncIterator[str],
    ) -> str:
        ...
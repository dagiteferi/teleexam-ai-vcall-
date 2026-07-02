from collections.abc import AsyncIterator
from typing import Protocol


class STTPort(Protocol):
    async def transcribe_stream(
        self,
        audio_stream: AsyncIterator[bytes],
    ) -> AsyncIterator[str]:
        ...
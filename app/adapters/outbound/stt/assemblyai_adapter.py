from collections.abc import AsyncIterator
import asyncio

import assemblyai as aai

from app.core.config import settings
from app.ports.stt_port import STTPort


class AssemblyAIAdapter(STTPort):
    def __init__(self) -> None:
        aai.settings.api_key = settings.assemblyai_api_key

    async def transcribe_stream(
        self,
        audio_stream: AsyncIterator[bytes],
    ) -> AsyncIterator[str]:
        queue: asyncio.Queue[str] = asyncio.Queue()

        def on_data(transcript: aai.RealtimeTranscript):
            if isinstance(transcript, aai.RealtimeFinalTranscript):
                queue.put_nowait(transcript.text)

        def on_error(error: aai.RealtimeError):
            print(f"AssemblyAI Error: {error}")

        transcriber = aai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=on_data,
            on_error=on_error,
        )

        transcriber.connect()

        try:
            async for chunk in audio_stream:
                transcriber.stream(chunk)

                while not queue.empty():
                    yield await queue.get()

        finally:
            transcriber.close()
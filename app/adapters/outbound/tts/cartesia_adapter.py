from collections.abc import AsyncIterator

from cartesia import Cartesia

from app.core.config import settings
from app.ports.tts_port import TTSPort


class CartesiaTTSAdapter(TTSPort):
    def __init__(self) -> None:
        self.client = Cartesia(api_key=settings.cartesia_api_key)

    async def speak_stream(
        self,
        text_stream: AsyncIterator[str],
    ) -> str:
        full_text = ""
        buffer = ""

        sentence_endings = {".", "!", "?", "\n"}

        async for token in text_stream:
            full_text += token
            buffer += token

            if buffer and buffer[-1] in sentence_endings:
                audio = self.client.tts.bytes(
                    model_id="sonic-english",
                    transcript=buffer.strip(),
                    voice_id="694f9389-aac1-45b6-b726-9d9369183238",
                    output_format={
                        "container": "wav",
                        "encoding": "pcm_s16le",
                        "sample_rate": 16000,
                    },
                )

                # TODO:
                # Send 'audio' to the LiveKit adapter once implemented.

                buffer = ""

        if buffer.strip():
            audio = self.client.tts.bytes(
                model_id="sonic-english",
                transcript=buffer.strip(),
                voice_id="694f9389-aac1-45b6-b726-9d9369183238",
                output_format={
                    "container": "wav",
                    "encoding": "pcm_s16le",
                    "sample_rate": 16000,
                },
            )

            # TODO:
            # Send remaining audio to LiveKit.

        return full_text
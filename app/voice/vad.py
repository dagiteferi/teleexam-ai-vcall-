import torch
import numpy as np


class SileroVAD:
    """
    Local voice activity detector using Silero VAD model.
    Detects when a user has finished speaking.
    """

    def __init__(self):
        (
            self.model,
            self.utils,
        ) = torch.hub.load(
            repo_or_dir="snakers4/silero-vad",
            model="silero_vad",
            force_reload=False,
            onnx=False,
        )

        (
            self.get_speech_timestamps,
            _,
            _,
            _,
            _,
        ) = self.utils


    def is_speech_complete(
        self,
        audio_buffer: bytes,
    ) -> bool:
        """
        Returns True when silence after speech is detected.
        """

        if not audio_buffer:
            return False


        audio = np.frombuffer(
            audio_buffer,
            dtype=np.int16,
        )


        audio_tensor = torch.from_numpy(
            audio.astype(np.float32)
        )


        speech_segments = self.get_speech_timestamps(
            audio_tensor,
            self.model,
        )


        if not speech_segments:
            return False


        last_segment = speech_segments[-1]


        silence_length = (
            len(audio_tensor)
            - last_segment["end"]
        )


        # approximately detects end of speech
        # based on silence after last speech segment
        return silence_length > 16000
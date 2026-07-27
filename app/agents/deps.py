from dataclasses import dataclass

from app.ports.llm_port import LLMPort
from app.ports.stt_port import STTPort
from app.ports.tts_port import TTSPort
from app.ports.embedding_port import EmbeddingPort
from app.ports.vector_search_port import VectorSearchPort
from app.ports.web_search_port import WebSearchPort
from app.ports.video_search_port import VideoSearchPort
from app.ports.cache_port import CachePort
from app.ports.media_session_port import MediaSessionPort
from app.ports.repositories import (
    CallSessionRepositoryPort,
    LearnerProfileRepositoryPort,
    CurriculumRepositoryPort,
)

# imports from app.ports.*

@dataclass
class AgentDependencies:
    llm: LLMPort
    stt: STTPort
    tts: TTSPort
    embeddings: EmbeddingPort
    vector_search: VectorSearchPort
    web_search: WebSearchPort
    video_search: VideoSearchPort
    cache: CachePort
    media: MediaSessionPort      # ← NEW
    call_repo: CallSessionRepositoryPort
    profile_repo: LearnerProfileRepositoryPort
    curriculum_repo: CurriculumRepositoryPort
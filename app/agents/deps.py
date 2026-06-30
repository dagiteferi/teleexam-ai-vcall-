from dataclasses import dataclass

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
    call_repo: CallSessionRepositoryPort
    profile_repo: LearnerProfileRepositoryPort
    curriculum_repo: CurriculumRepositoryPort
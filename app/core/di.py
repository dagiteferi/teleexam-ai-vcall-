from app.agents.deps import AgentDependencies
from app.core.config import Settings, settings

from app.adapters.outbound.llm.groq_adapter import GroqLLMAdapter
from app.adapters.outbound.llm.cerebras_adapter import CerebrasLLMAdapter

from app.adapters.outbound.stt.assemblyai_adapter import AssemblyAIAdapter
from app.adapters.outbound.stt.deepgram_adapter import DeepgramAdapter
from app.adapters.outbound.stt.groq_whisper_adapter import GroqWhisperAdapter

from app.adapters.outbound.tts.cartesia_adapter import CartesiaTTSAdapter
from app.adapters.outbound.tts.elevenlabs_adapter import ElevenLabsAdapter

from app.adapters.outbound.embeddings.voyage_adapter import VoyageAdapter
from app.adapters.outbound.embeddings.cohere_adapter import CohereAdapter

from app.adapters.outbound.search.tavily_adapter import TavilyAdapter
from app.adapters.outbound.video.youtube_adapter import YouTubeAdapter

from app.adapters.outbound.cache.redis_adapter import RedisAdapter

from app.adapters.outbound.db.postgres_call_repo import PostgresCallRepository
from app.adapters.outbound.db.postgres_profile_repo import PostgresProfileRepository
from app.adapters.outbound.db.postgres_curriculum_repo import PostgresCurriculumRepository

def build_dependencies(settings: Settings) -> AgentDependencies:
    if settings.llm_provider == "groq":
        llm = GroqLLMAdapter()
    else:
        llm = CerebrasLLMAdapter()

    if settings.stt_provider == "assemblyai":
        stt = AssemblyAIAdapter()
    elif settings.stt_provider == "deepgram":
        stt = DeepgramAdapter()
    else:
        stt = GroqWhisperAdapter()

    if settings.tts_provider == "cartesia":
        tts = CartesiaTTSAdapter()
    else:
        tts = ElevenLabsAdapter()

    if settings.embedding_provider == "voyage":
        embeddings = VoyageAdapter()
    else:
        embeddings = CohereAdapter()

    web_search = TavilyAdapter()
    video_search = YouTubeAdapter()
    media = LiveKitAdapter()
    cache = RedisAdapter()

    call_repo = PostgresCallRepository()
    profile_repo = PostgresProfileRepository()
    curriculum_repo = PostgresCurriculumRepository()

    return AgentDependencies(
        llm=llm,
        stt=stt,
        tts=tts,
        embeddings=embeddings,
        vector_search=None,
        web_search=web_search,
        video_search=video_search,
        cache=cache,
        call_repo=call_repo,
        profile_repo=profile_repo,
        curriculum_repo=curriculum_repo,
    )


dependencies = build_dependencies(settings)
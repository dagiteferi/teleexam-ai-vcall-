from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.deps import AgentDependencies
from app.core.config import Settings, settings
from app.core.database import async_session

# LLM
from app.adapters.outbound.llm.groq_adapter import GroqLLMAdapter

# STT
from app.adapters.outbound.stt.assemblyai_adapter import AssemblyAIAdapter

# TTS
from app.adapters.outbound.tts.cartesia_adapter import CartesiaTTSAdapter

# Embeddings
from app.adapters.outbound.embeddings.voyage_adapter import VoyageAdapter

# Search
from app.adapters.outbound.search.tavily_adapter import TavilyAdapter

# Video
from app.adapters.outbound.video.youtube_adapter import YouTubeAdapter

# Cache
from app.adapters.outbound.cache.redis_adapter import RedisAdapter

# Media
from app.adapters.outbound.media.livekit_adapter import LiveKitAdapter

# Database
from app.adapters.outbound.db.postgres_call_repo import (
    PostgresCallRepository,
)

from app.adapters.outbound.db.postgres_profile_repo import (
    PostgresProfileRepository,
)

from app.adapters.outbound.db.postgres_curriculum_repo import (
    PostgresCurriculumRepository,
)

from app.adapters.outbound.db.postgres_vector_search import (
    PostgresVectorSearchAdapter,
)


def build_dependencies(
    settings: Settings,
    session: AsyncSession,
) -> AgentDependencies:

    # LLM
    llm = GroqLLMAdapter(
        model=settings.groq_model,
    )

    # STT
    stt = AssemblyAIAdapter()

    # TTS
    tts = CartesiaTTSAdapter()

    # Embeddings
    embeddings = VoyageAdapter(settings)

    # Vector Search
    vector_search = PostgresVectorSearchAdapter(
        session=session,
    )

    # Web Search
    web_search = TavilyAdapter(settings)

    # Video Search
    video_search = YouTubeAdapter()

    # Cache
    cache = RedisAdapter(
        host=settings.redis_host,
        port=settings.redis_port,
    )

    # LiveKit Media
    media = LiveKitAdapter(
        url=settings.livekit_url,
        api_key=settings.livekit_api_key,
        api_secret=settings.livekit_api_secret,
    )

    # Repositories
    call_repo = PostgresCallRepository(
        session=session,
    )

    profile_repo = PostgresProfileRepository(
        session=session,
    )

    curriculum_repo = PostgresCurriculumRepository(
        session=session,
    )


    return AgentDependencies(
        llm=llm,
        stt=stt,
        tts=tts,
        embeddings=embeddings,
        vector_search=vector_search,
        web_search=web_search,
        video_search=video_search,
        cache=cache,
        media=media,
        call_repo=call_repo,
        profile_repo=profile_repo,
        curriculum_repo=curriculum_repo,
    )


async def get_dependencies():
    async with async_session() as session:

        deps = build_dependencies(
            settings=settings,
            session=session,
        )

        yield deps


dependencies = get_dependencies
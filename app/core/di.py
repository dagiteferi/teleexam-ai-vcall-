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

    llm = GroqLLMAdapter(
        model=settings.groq_model,
    )

    stt = AssemblyAIAdapter()

    tts = CartesiaTTSAdapter()

    embeddings = VoyageAdapter(settings)

    vector_search = PostgresVectorSearchAdapter(
        session=session,
    )

    web_search = TavilyAdapter(settings)

    video_search = YouTubeAdapter()

    cache = RedisAdapter(
        host=settings.redis_host,
        port=settings.redis_port,
    )

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
        call_repo=call_repo,
        profile_repo=profile_repo,
        curriculum_repo=curriculum_repo,
    )


async def get_dependencies() -> AgentDependencies:
    async with async_session() as session:
        return build_dependencies(
            settings=settings,
            session=session,
        )


dependencies = get_dependencies
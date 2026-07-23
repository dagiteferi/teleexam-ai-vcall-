from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.tables import CurriculumChunkTable
from app.domain.models import CurriculumChunk
from app.ports.repositories import CurriculumRepositoryPort


class PostgresCurriculumRepository(
    CurriculumRepositoryPort
):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_chunk(
        self,
        chunk: CurriculumChunk,
    ) -> None:

        db_chunk = CurriculumChunkTable(
            chunk_id=chunk.chunk_id,
            topic=chunk.topic,
            content=chunk.content,
            source=chunk.source,
            embedding=chunk.embedding,
            created_at=chunk.created_at,
        )

        self.session.add(db_chunk)
        await self.session.commit()

    async def get_all_chunks(
        self,
    ) -> list[CurriculumChunk]:

        result = await self.session.execute(
            select(CurriculumChunkTable)
        )

        rows = result.scalars().all()

        return [
            CurriculumChunk(
                chunk_id=row.chunk_id,
                topic=row.topic,
                content=row.content,
                source=row.source,
                embedding=row.embedding,
                created_at=row.created_at,
            )
            for row in rows
        ]
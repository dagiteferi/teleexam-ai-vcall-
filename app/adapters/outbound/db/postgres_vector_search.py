from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.tables import CurriculumChunkTable
from app.ports.vector_search_port import VectorSearchPort


class PostgresVectorSearchAdapter(VectorSearchPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(
        self,
        query_embedding: list[float],
        k: int = 5,
    ) -> list[str]:

        distance = CurriculumChunkTable.embedding.cosine_distance(
            query_embedding
        )

        stmt = (
            select(CurriculumChunkTable.content)
            .order_by(distance)
            .limit(k)
        )

        result = await self.session.execute(stmt)

        return [
            row[0]
            for row in result.all()
        ]
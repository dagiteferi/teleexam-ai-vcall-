from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import LearnerProfile
from app.ports.repositories import LearnerProfileRepositoryPort


class PostgresProfileRepository(
    LearnerProfileRepositoryPort
):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(
        self,
        telegram_id: int,
    ) -> LearnerProfile | None:

        query = text(
            """
            SELECT
                id AS user_id,
                telegram_id,
                weak_topics,
                avg_score,
                exams_done,
                last_seen_at

            FROM learner_profiles

            WHERE telegram_id = :telegram_id
            """
        )

        result = await self.session.execute(
            query,
            {
                "telegram_id": telegram_id,
            },
        )

        row = result.mappings().one_or_none()

        if row is None:
            return None

        return LearnerProfile(
            user_id=row["user_id"],
            telegram_id=row["telegram_id"],
            weak_topics=row["weak_topics"] or [],
            avg_score=float(row["avg_score"] or 0),
            exams_done=row["exams_done"] or 0,
            last_seen_at=row["last_seen_at"],
        )

    async def create(
        self,
        telegram_id: int,
    ) -> None:

        query = text(
            """
            INSERT INTO learner_profiles (
                telegram_id,
                weak_topics,
                avg_score,
                exams_done
            )
            VALUES (
                :telegram_id,
                ARRAY[]::text[],
                0,
                0
            )
            ON CONFLICT (telegram_id)
            DO NOTHING
            """
        )

        await self.session.execute(
            query,
            {
                "telegram_id": telegram_id,
            },
        )

        await self.session.commit()
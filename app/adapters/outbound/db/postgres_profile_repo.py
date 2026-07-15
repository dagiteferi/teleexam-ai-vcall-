# READ-ONLY — never write to TeleExam monolith tables

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
                u.id AS user_id,
                u.telegram_id,
                COALESCE(
                    ARRAY_AGG(
                        ute.topic
                    ) FILTER (
                        WHERE ute.topic IS NOT NULL
                    ),
                    '{}'
                ) AS weak_topics,
                COALESCE(
                    AVG(er.score),
                    0
                ) AS avg_score,
                COUNT(er.id) AS exams_done,
                MAX(u.last_seen_at) AS last_seen_at

            FROM users u

            LEFT JOIN user_topic_errors ute
                ON ute.user_id = u.id

            LEFT JOIN exam_results er
                ON er.user_id = u.id

            WHERE u.telegram_id = :telegram_id

            GROUP BY u.id
            """
        )

        result = await self.session.execute(
            query,
            {
                "telegram_id": telegram_id
            },
        )

        row = result.mappings().one_or_none()

        if row is None:
            return None

        return LearnerProfile(
            user_id=row["user_id"],
            telegram_id=row["telegram_id"],
            weak_topics=row["weak_topics"],
            avg_score=float(row["avg_score"]),
            exams_done=row["exams_done"],
            last_seen_at=row["last_seen_at"],
        )
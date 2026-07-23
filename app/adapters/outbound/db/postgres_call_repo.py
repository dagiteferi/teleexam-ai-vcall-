from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.tables import CallSessionTable, CallTurnTable
from app.domain.models import CallSession, Turn
from app.ports.repositories import CallSessionRepositoryPort


class PostgresCallRepository(CallSessionRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, session: CallSession) -> None:
        db_session = CallSessionTable(
            session_id=session.session_id,
            user_id=session.user_id,
            telegram_id=session.telegram_id,
            room_name=session.room_name,
            status=session.status,
            started_at=session.started_at,
            ended_at=session.ended_at,
        )

        self.session.add(db_session)
        await self.session.commit()

    async def get_by_id(
        self,
        session_id: str,
    ) -> CallSession | None:

        result = await self.session.execute(
            select(CallSessionTable).where(
                CallSessionTable.session_id == session_id
            )
        )

        row = result.scalar_one_or_none()

        if row is None:
            return None

        return CallSession(
            session_id=row.session_id,
            user_id=row.user_id,
            telegram_id=row.telegram_id,
            room_name=row.room_name,
            status=row.status,
            started_at=row.started_at,
            ended_at=row.ended_at,
        )

    async def update_status(
        self,
        session_id: str,
        status: str,
    ) -> None:

        values = {
            "status": status,
        }

        if status == "ended":
            values["ended_at"] = datetime.now(UTC)

        await self.session.execute(
            update(CallSessionTable)
            .where(
                CallSessionTable.session_id == session_id
            )
            .values(**values)
        )

        await self.session.commit()

    async def save_turn(self, turn: Turn) -> None:
        db_turn = CallTurnTable(
            turn_id=turn.turn_id,
            session_id=turn.session_id,
            transcript=turn.transcript,
            intent=turn.intent,
            ai_response=turn.ai_response,
            latency_ms=turn.latency_ms,
            created_at=turn.created_at,
        )

        self.session.add(db_turn)
        await self.session.commit()
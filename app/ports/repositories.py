from typing import Optional, Protocol

from app.domain.models import (
    CallSession,
    CurriculumChunk,
    LearnerProfile,
    Turn,
)


class CallSessionRepositoryPort(Protocol):
    async def save(
        self,
        session: CallSession,
    ) -> None:
        ...

    async def get_by_id(
        self,
        session_id: str,
    ) -> Optional[CallSession]:
        ...

    async def update_status(
        self,
        session_id: str,
        status: str,
    ) -> None:
        ...

    async def save_turn(
        self,
        turn: Turn,
    ) -> None:
        ...


class LearnerProfileRepositoryPort(Protocol):
    async def get_by_telegram_id(
        self,
        telegram_id: int,
    ) -> Optional[LearnerProfile]:
        ...


class CurriculumRepositoryPort(Protocol):
    async def save_chunk(
        self,
        chunk: CurriculumChunk,
    ) -> None:
        ...
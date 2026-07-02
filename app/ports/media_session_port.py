from typing import Protocol


class MediaSessionPort(Protocol):
    async def create_room(
        self,
        room_name: str,
    ) -> None:
        ...

    async def create_token(
        self,
        room_name: str,
        user_id: str,
    ) -> str:
        ...
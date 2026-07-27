from livekit import api

from app.ports.media_session_port import MediaSessionPort


class LiveKitAdapter(MediaSessionPort):

    def __init__(
        self,
        url: str,
        api_key: str | None,
        api_secret: str | None,
    ):
        self.url = url
        self.api_key = api_key
        self.api_secret = api_secret

        if not api_key or not api_secret:
            raise ValueError(
                "LiveKit API key and secret are required"
            )


    async def create_room(
        self,
        room_name: str,
    ) -> None:

        # LiveKit creates rooms automatically when
        # the first participant joins.
        #
        # This method exists because our architecture
        # requires a room creation step.

        room_service = api.LiveKitAPI(
            self.url,
            self.api_key,
            self.api_secret,
        )

        await room_service.room.create_room(
            api.CreateRoomRequest(
                name=room_name
            )
        )

        await room_service.aclose()


    async def create_token(
        self,
        room_name: str,
        user_id: str,
    ) -> str:

        token = (
            api.AccessToken(
                self.api_key,
                self.api_secret,
            )
            .with_identity(user_id)
            .with_name(user_id)
            .with_grants(
                api.VideoGrants(
                    room_join=True,
                    room=room_name,
                )
            )
        )

        return token.to_jwt()
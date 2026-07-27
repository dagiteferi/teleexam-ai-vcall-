from livekit import api

from app.ports.media_session_port import MediaSessionPort


class LiveKitAdapter(MediaSessionPort):

    def __init__(
        self,
        url: str,
        api_key: str | None,
        api_secret: str | None,
    ):
        if not api_key or not api_secret:
            raise ValueError(
                "LiveKit credentials missing"
            )

        self.url = url
        self.api_key = api_key
        self.api_secret = api_secret


    async def create_room(
        self,
        room_name: str,
    ) -> None:

        client = api.LiveKitAPI(
            self.url,
            self.api_key,
            self.api_secret,
        )

        try:

            await client.room.create_room(
                api.CreateRoomRequest(
                    name=room_name
                )
            )

        except Exception as e:

            # Ignore existing rooms
            if "already exists" not in str(e).lower():
                raise

        finally:
            await client.aclose()



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
                    can_publish=True,
                    can_subscribe=True,
                )
            )
        )

        return token.to_jwt()
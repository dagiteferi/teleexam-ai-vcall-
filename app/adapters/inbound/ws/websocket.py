from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)

from app.agents.deps import AgentDependencies
from app.application.process_turn import process_turn
from app.application.end_call_session import end_call_session
from app.core.di import get_dependencies


router = APIRouter(
    tags=["websocket"],
)


@router.websocket("/ws/{session_id}")
async def websocket_handler(
    websocket: WebSocket,
    session_id: str,
    telegram_id: int,
    deps: AgentDependencies = Depends(get_dependencies),
):
    """
    Real-time WebSocket endpoint.

    Flow:
    1. Verify session ownership.
    2. Accept the connection.
    3. Process incoming messages.
    4. Clean up when disconnected.
    """

    # -------------------------------------------------
    # STEP 1 — Verify session ownership BEFORE accept()
    # -------------------------------------------------

    session = await deps.call_repo.get_by_id(
        session_id
    )

    if (
        session is None
        or session.telegram_id != telegram_id
    ):
        await websocket.close(
            code=4403
        )
        return

    # Connection is trusted.
    await websocket.accept()

    # -------------------------------------------------
    # STEP 2 — Message loop
    # -------------------------------------------------

    try:

        while True:

            message = await websocket.receive_json()

            message_type = message.get("type")

            # -----------------------------
            # ping
            # -----------------------------
            if message_type == "ping":

                await websocket.send_json(
                    {
                        "type": "pong",
                    }
                )

            # -----------------------------
            # transcript
            # -----------------------------
            elif message_type == "transcript":

                result = await process_turn(
                    session_id=session_id,
                    transcript=message["text"],
                    telegram_id=telegram_id,
                    user_id=session.user_id,
                    deps=deps,
                )

                await websocket.send_json(
                    {
                        "type": "response",
                        "text": result["ai_response"],
                        "intent": result["intent"],
                        "latency_ms": result["latency_ms"],
                    }
                )

            # -----------------------------
            # audio chunk
            # -----------------------------
            elif message_type == "audio_chunk":

                await websocket.send_json(
                    {
                        "type": "audio_received",
                    }
                )

    # -------------------------------------------------
    # STEP 3 — Cleanup
    # -------------------------------------------------

    except WebSocketDisconnect:

        await end_call_session(
            session_id=session_id,
            deps=deps,
        )
        
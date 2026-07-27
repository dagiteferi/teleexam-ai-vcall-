from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.agents.deps import AgentDependencies
from app.application.start_call_session import (
    start_call_session,
)
from app.application.end_call_session import (
    end_call_session,
)
from app.core.di import get_dependencies


router = APIRouter(
    tags=["sessions"],
)


class StartSessionRequest(BaseModel):
    telegram_id: int
    user_id: int


@router.post("/sessions/start")
async def start_session(
    request: StartSessionRequest,
    deps: AgentDependencies = Depends(get_dependencies),
):

    session = await start_call_session(
        telegram_id=request.telegram_id,
        user_id=request.user_id,
        deps=deps,
    )


    token = await deps.media.create_token(
        room_name=session.room_name,
        user_id=str(request.user_id),
    )


    return {
        "session": session,
        "token": token,
    }



@router.post("/sessions/{session_id}/end")
async def end_session(
    session_id: str,
    deps: AgentDependencies = Depends(get_dependencies),
):

    await end_call_session(
        session_id=session_id,
        deps=deps,
    )


    return {
        "status": "ended"
    }



@router.get("/sessions/{session_id}")
async def get_session(
    session_id: str,
    deps: AgentDependencies = Depends(get_dependencies),
):

    session = await deps.call_repo.get_by_id(
        session_id
    )


    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )


    return session
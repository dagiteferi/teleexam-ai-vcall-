from fastapi import APIRouter, Depends, HTTPException

from app.agents.deps import AgentDependencies
from app.core.di import get_dependencies

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{telegram_id}/profile")
async def get_profile(
    telegram_id: int,
    deps: AgentDependencies = Depends(get_dependencies),
):
    profile = await deps.profile_repo.get_by_telegram_id(
        telegram_id
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return profile
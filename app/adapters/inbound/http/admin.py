from fastapi import APIRouter, Depends, Header, HTTPException

from app.application.ingest_curriculum import ingest_curriculum
from app.core.config import settings

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.post("/ingest")
async def ingest(
    x_admin_key: str | None = Header(default=None),
):
    if (
        settings.admin_api_key is None
        or x_admin_key != settings.admin_api_key
    ):
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

    await ingest_curriculum()

    return {
        "status": "ingestion started",
    }
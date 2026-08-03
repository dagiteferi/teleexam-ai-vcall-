from fastapi import FastAPI

from app.core.config import settings

from app.adapters.inbound.http.sessions import router as sessions_router
from app.adapters.inbound.http.users import router as users_router
from app.adapters.inbound.http.admin import router as admin_router
from app.adapters.inbound.ws.websocket import router as websocket_router


app = FastAPI(
    title="TeleExam AI — Video Call Tutor",
    description=(
        "AI-powered real-time tutoring for Ethiopian CS exit exam students"
    ),
    version="2.0.0",
)


@app.on_event("startup")
async def startup_event():
    print(
        "TeleExam AI Video Call Tutor started"
    )

    print(
        f"LLM provider: {settings.llm_provider}"
    )

    print(
        f"STT provider: {settings.stt_provider}"
    )

    print(
        f"TTS provider: {settings.tts_provider}"
    )

    print(
        f"Embedding provider: {settings.embedding_provider}"
    )


# HTTP routers

app.include_router(
    sessions_router,
    prefix="/vcall",
)

app.include_router(
    users_router,
    prefix="/vcall",
)

app.include_router(
    admin_router,
    prefix="/vcall/admin",
)


# WebSocket router

app.include_router(
    websocket_router,
    prefix="/vcall",
)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "vcall-service",
        "version": "2.0.0",
    }
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
class CallSession(BaseModel):
    session_id: str
    user_id: int
    telegram_id: int
    room_name: str
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None

class Turn(BaseModel):
    turn_id: str
    session_id: str
    transcript: str
    intent: str
    ai_response: str
    latency_ms: int
    created_at: datetime
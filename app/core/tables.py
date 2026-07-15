from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.core.database import Base


class CallSessionTable(Base):
    __tablename__ = "call_sessions"

    session_id = Column(String, primary_key=True)
    user_id = Column(Integer, nullable=False)
    telegram_id = Column(BigInteger, nullable=False)
    room_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)


class CallTurnTable(Base):
    __tablename__ = "call_turns"

    turn_id = Column(String, primary_key=True)
    session_id = Column(
        String,
        ForeignKey("call_sessions.session_id"),
        nullable=False,
    )
    transcript = Column(Text, nullable=False)
    intent = Column(String, nullable=False)
    ai_response = Column(Text, nullable=False)
    latency_ms = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class CurriculumChunkTable(Base):
    __tablename__ = "curriculum_chunks"

    chunk_id = Column(String, primary_key=True)
    topic = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String, nullable=False)
    embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
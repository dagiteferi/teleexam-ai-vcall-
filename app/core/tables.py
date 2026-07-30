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

from sqlalchemy.dialects.postgresql import ARRAY

from app.core.database import Base


class CallSessionTable(Base):
    __tablename__ = "call_sessions"

    session_id = Column(String, primary_key=True)

    user_id = Column(
        Integer,
        nullable=False,
    )

    telegram_id = Column(
        BigInteger,
        nullable=False,
    )

    room_name = Column(
        String,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    ended_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )


class CallTurnTable(Base):
    __tablename__ = "call_turns"

    turn_id = Column(
        String,
        primary_key=True,
    )

    session_id = Column(
        String,
        ForeignKey("call_sessions.session_id"),
        nullable=False,
    )

    transcript = Column(
        Text,
        nullable=False,
    )

    intent = Column(
        String,
        nullable=False,
    )

    ai_response = Column(
        Text,
        nullable=False,
    )

    latency_ms = Column(
        Integer,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )


class CurriculumChunkTable(Base):
    __tablename__ = "curriculum_chunks"

    chunk_id = Column(
        String,
        primary_key=True,
    )

    topic = Column(
        String,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    source = Column(
        String,
        nullable=False,
    )

    embedding = Column(
        Vector(1024),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )


class LearnerProfileTable(Base):
    __tablename__ = "learner_profiles"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    telegram_id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        index=True,
    )

    weak_topics = Column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    avg_score = Column(
        Integer,
        nullable=False,
        default=0,
    )

    exams_done = Column(
        Integer,
        nullable=False,
        default=0,
    )

    last_seen_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )
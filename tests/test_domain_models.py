from datetime import datetime

from app.domain.models import (
    CallSession,
    Turn,
    LearnerProfile,
    CurriculumChunk,
)


def test_create_valid_call_session():
    session = CallSession(
        session_id="session_001",
        user_id=1,
        telegram_id=123456789,
        room_name="exam_room",
        status="active",
        started_at=datetime.now(),
        ended_at=None,
    )

    assert session.session_id == "session_001"
    assert session.user_id == 1
    assert session.telegram_id == 123456789
    assert session.room_name == "exam_room"
    assert session.status == "active"
    assert session.ended_at is None


def test_call_session_model_dump():
    session = CallSession(
        session_id="session_001",
        user_id=1,
        telegram_id=123456789,
        room_name="exam_room",
        status="active",
        started_at=datetime.now(),
    )

    data = session.model_dump()

    assert isinstance(data, dict)
    assert data["session_id"] == "session_001"
    assert data["user_id"] == 1


def test_create_valid_turn():
    turn = Turn(
        turn_id="turn_001",
        session_id="session_001",
        transcript="What is Python?",
        intent="exam_question",
        ai_response="Python is a programming language.",
        latency_ms=250,
        created_at=datetime.now(),
    )

    assert turn.turn_id == "turn_001"
    assert turn.session_id == "session_001"
    assert turn.transcript == "What is Python?"
    assert turn.intent == "exam_question"
    assert turn.ai_response == "Python is a programming language."
    assert turn.latency_ms == 250


def test_turn_model_dump():
    turn = Turn(
        turn_id="turn_001",
        session_id="session_001",
        transcript="Hello",
        intent="greeting",
        ai_response="Hi!",
        latency_ms=120,
        created_at=datetime.now(),
    )

    data = turn.model_dump()

    assert isinstance(data, dict)
    assert data["turn_id"] == "turn_001"
    assert data["intent"] == "greeting"
    assert data["latency_ms"] == 120


def test_create_valid_learner_profile():
    profile = LearnerProfile(
        user_id=1,
        telegram_id=123456789,
        weak_topics=["Math", "Physics", "Chemistry"],
        avg_score=82.5,
        exams_done=4,
        last_seen_at=datetime.now(),
    )

    assert profile.user_id == 1
    assert profile.telegram_id == 123456789
    assert profile.weak_topics == ["Math", "Physics", "Chemistry"]
    assert profile.avg_score == 82.5
    assert profile.exams_done == 4


def test_learner_profile_default_last_seen():
    profile = LearnerProfile(
        user_id=2,
        telegram_id=987654321,
        weak_topics=["Biology"],
        avg_score=75.0,
        exams_done=2,
    )

    assert profile.last_seen_at is None


def test_create_curriculum_chunk_with_embedding():
    chunk = CurriculumChunk(
        chunk_id="chunk_001",
        topic="Data Structures",
        content="A stack follows the LIFO principle.",
        source="chapter4.pdf",
        embedding=[0.12, 0.45, -0.33],
    )

    assert chunk.chunk_id == "chunk_001"
    assert chunk.topic == "Data Structures"
    assert chunk.embedding == [0.12, 0.45, -0.33]


def test_curriculum_chunk_default_embedding():
    chunk = CurriculumChunk(
        chunk_id="chunk_002",
        topic="Algorithms",
        content="Binary search is efficient.",
        source="algorithms.pdf",
    )

    assert chunk.embedding is None
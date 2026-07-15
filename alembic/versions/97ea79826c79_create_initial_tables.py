"""create initial tables

Revision ID: 97ea79826c79
Revises:
Create Date: 2026-07-15 11:53:38.999812

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "97ea79826c79"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension before creating vector columns
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Stores every AI video call session
    op.create_table(
        "call_sessions",
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("room_name", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "ended_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("session_id"),
    )

    # Stores every conversation exchange during a call
    op.create_table(
        "call_turns",
        sa.Column("turn_id", sa.String(), nullable=False),
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column("transcript", sa.Text(), nullable=False),
        sa.Column("intent", sa.String(), nullable=False),
        sa.Column("ai_response", sa.Text(), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["call_sessions.session_id"],
        ),
        sa.PrimaryKeyConstraint("turn_id"),
    )

    # Stores curriculum chunks and embeddings for RAG similarity search
    op.create_table(
        "curriculum_chunks",
        sa.Column("chunk_id", sa.String(), nullable=False),
        sa.Column("topic", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column(
            "embedding",
            Vector(1536),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("chunk_id"),
    )


def downgrade() -> None:
    op.drop_table("curriculum_chunks")
    op.drop_table("call_turns")
    op.drop_table("call_sessions")
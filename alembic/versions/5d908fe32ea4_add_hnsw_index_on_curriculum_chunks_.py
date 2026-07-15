"""add hnsw index on curriculum chunks embedding

Revision ID: 5d908fe32ea4
Revises: 97ea79826c79
Create Date: 2026-07-15 13:28:43.539222

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "5d908fe32ea4"
down_revision: Union[str, None] = "97ea79826c79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE INDEX curriculum_chunks_embedding_hnsw_idx
        ON curriculum_chunks
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64)
    """)


def downgrade() -> None:
    op.execute(
        "DROP INDEX IF EXISTS curriculum_chunks_embedding_hnsw_idx"
    )
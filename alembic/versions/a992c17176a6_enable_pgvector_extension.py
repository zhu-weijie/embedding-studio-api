"""Enable pgvector extension

Revision ID: a992c17176a6
Revises: ee199c0b549f
Create Date: 2025-08-03 16:18:08.767388

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a992c17176a6"
down_revision: Union[str, Sequence[str], None] = "ee199c0b549f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP EXTENSION vector")

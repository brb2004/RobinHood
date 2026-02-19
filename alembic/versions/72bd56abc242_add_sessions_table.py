"""add sessions table

Revision ID: 72bd56abc242
Revises: 67cba4fd2570
Create Date: 2026-02-19 01:20:14.049534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72bd56abc242'
down_revision: Union[str, Sequence[str], None] = '67cba4fd2570'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("sessions",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    sa.Column("session_token", sa.String(255), nullable=False, unique=True),
    sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("sessions")

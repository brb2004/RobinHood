"""create users table

Revision ID: dd09965d863f
Revises: 
Create Date: 2026-02-19 00:06:22.163118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd09965d863f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("users",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String(50), nullable=False, unique=True),
    sa.Column("email", sa.String(120), nullable=False, unique=True),
    sa.Column("password_hash", sa.String(128), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")

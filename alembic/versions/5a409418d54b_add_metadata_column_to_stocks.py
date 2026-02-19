"""add metadata column to stocks

Revision ID: 5a409418d54b
Revises: 2da13d8820ce
Create Date: 2026-02-19 00:21:51.750117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a409418d54b'
down_revision: Union[str, Sequence[str], None] = '2da13d8820ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("stocks",
    sa.Column("Metadata", sa.String(255), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("stocks", "Metadata")

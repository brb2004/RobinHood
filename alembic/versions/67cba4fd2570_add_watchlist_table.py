"""add watchlist table

Revision ID: 67cba4fd2570
Revises: 5a409418d54b
Create Date: 2026-02-19 00:34:06.225432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67cba4fd2570'
down_revision: Union[str, Sequence[str], None] = '5a409418d54b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass

def downgrade() -> None:
    """Downgrade schema."""
    pass

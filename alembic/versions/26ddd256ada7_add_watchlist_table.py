"""add watchlist table

Revision ID: 26ddd256ada7
Revises: 747a8b601dfc
Create Date: 2026-02-20 14:10:41.441732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26ddd256ada7'
down_revision: Union[str, Sequence[str], None] = '747a8b601dfc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'watchlist',
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('symbol', sa.String(10), primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

    op.create_foreign_key(
        'fk_watchlist_user_id_users',
        'watchlist', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

    op.create_foreign_key(
        'fk_watchlist_symbol_companies',
        'watchlist', 'companies',
        ['symbol'], ['symbol'],
        ondelete='CASCADE'
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('watchlist')

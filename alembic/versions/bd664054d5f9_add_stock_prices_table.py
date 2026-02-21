"""add stock_prices table

Revision ID: bd664054d5f9
Revises: 26ddd256ada7
Create Date: 2026-02-20 14:16:23.618614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd664054d5f9'
down_revision: Union[str, Sequence[str], None] = '26ddd256ada7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'stock_prices',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('symbol', sa.String(10), nullable=False),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('percent_change', sa.Numeric(6, 3), nullable=True),
        sa.Column('volume', sa.BigInteger, nullable=True),
        sa.Column('market_timestamp', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    # Indexes
    op.create_index('ix_stock_prices_symbol', 'stock_prices', ['symbol'])
    op.create_index('ix_stock_prices_market_timestamp', 'stock_prices', ['market_timestamp'])

    # Unique constraint
    op.create_unique_constraint(
        'uq_stock_prices_symbol_market_timestamp',
        'stock_prices',
        ['symbol', 'market_timestamp']
    )

    # Foreign key
    op.create_foreign_key(
        'fk_stock_prices_symbol_companies',
        'stock_prices',
        'companies',
        ['symbol'],
        ['symbol'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('stock_prices')
"""create stocks table

Revision ID: 2da13d8820ce
Revises: dd09965d863f
Create Date: 2026-02-19 00:13:26.406707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2da13d8820ce'
down_revision: Union[str, Sequence[str], None] = 'dd09965d863f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("stocks",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("symbol", sa.String(10), nullable=False, unique=True),
    sa.Column("company_name", sa.String(100), nullable=False),
    sa.Column("price", sa.Float, nullable=False),
    sa.Column("date", sa.Date, nullable=False),
    sa.Column("percent_change", sa.Float, nullable=False))
    sa.Column("Metadata", sa.String(255), nullable=True)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("stocks")

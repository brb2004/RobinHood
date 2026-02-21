"""add companies table

Revision ID: 747a8b601dfc
Revises: 89942aded1ba
Create Date: 2026-02-20 14:07:32.981494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '747a8b601dfc'
down_revision: Union[str, Sequence[str], None] = '89942aded1ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('symbol', sa.String(10), nullable=False, unique=True),
        sa.Column('company_name', sa.String(100), nullable=False, unique=True),
        sa.Column("exchange", sa.String(10), nullable=False),
        sa.Column('sector', sa.String(50), nullable=True),
        sa.Column('industry', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()))
    

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('companies')

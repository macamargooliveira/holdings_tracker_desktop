"""create currencies

Revision ID: 1319f6073c95
Revises: b41afe708661
Create Date: 2025-12-26 14:21:17.483694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1319f6073c95'
down_revision: Union[str, Sequence[str], None] = 'b41afe708661'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('currencies',
    sa.Column('code', sa.String(length=3), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('symbol', sa.String(length=3), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_currencies_id'), 'currencies', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_currencies_id'), table_name='currencies')
    op.drop_table('currencies')

"""create asset events

Revision ID: 007
Revises: 006
Create Date: 2026-01-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '007'
down_revision: Union[str, Sequence[str], None] = '006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('asset_events',
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('event_type', sa.Enum('SPLIT', 'REVERSE_SPLIT', 'AMORTIZATION', 'SUBSCRIPTION', 'CONVERSION', name='asseteventtype'), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('factor', sa.Numeric(precision=10, scale=6), nullable=True),
    sa.Column('quantity', sa.Numeric(precision=20, scale=6), nullable=True),
    sa.Column('price', sa.Numeric(precision=20, scale=6), nullable=True),
    sa.Column('converted_to_asset_id', sa.Integer(), nullable=True),
    sa.Column('conversion_quantity', sa.Numeric(precision=20, scale=6), nullable=True),
    sa.Column('residual_value', sa.Numeric(precision=20, scale=6), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.ForeignKeyConstraint(['converted_to_asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_asset_events_id'), 'asset_events', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_asset_events_id'), table_name='asset_events')
    op.drop_table('asset_events')

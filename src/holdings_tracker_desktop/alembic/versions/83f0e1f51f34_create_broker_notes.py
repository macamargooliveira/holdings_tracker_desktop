"""create broker notes

Revision ID: 83f0e1f51f34
Revises: 5e9f6cf6a1f1
Create Date: 2025-12-26 14:30:25.026143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83f0e1f51f34'
down_revision: Union[str, Sequence[str], None] = '5e9f6cf6a1f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('broker_notes',
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('operation', sa.Enum('BUY', 'SELL', name='operationtype'), nullable=False),
    sa.Column('broker_id', sa.Integer(), nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('price', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('fees', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('taxes', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('note_number', sa.String(length=30), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.ForeignKeyConstraint(['broker_id'], ['brokers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_broker_notes_id'), 'broker_notes', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_broker_notes_id'), table_name='broker_notes')
    op.drop_table('broker_notes')

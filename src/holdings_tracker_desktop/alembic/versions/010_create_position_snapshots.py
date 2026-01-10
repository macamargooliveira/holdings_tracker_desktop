"""create position snapshots

Revision ID: 010
Revises: 009
Create Date: 2026-01-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '010'
down_revision: Union[str, Sequence[str], None] = '009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('position_snapshots',
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('snapshot_date', sa.Date(), nullable=False),
    sa.Column('quantity', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('avg_price', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_position_snapshots_id'), 'position_snapshots', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_position_snapshots_id'), table_name='position_snapshots')
    op.drop_table('position_snapshots')

"""create asset ticker histories

Revision ID: 5e9f6cf6a1f1
Revises: b5dc34cb1199
Create Date: 2025-12-26 14:29:48.910669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e9f6cf6a1f1'
down_revision: Union[str, Sequence[str], None] = 'b5dc34cb1199'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('asset_ticker_histories',
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('old_ticker', sa.String(length=5), nullable=False),
    sa.Column('new_ticker', sa.String(length=5), nullable=False),
    sa.Column('change_date', sa.Date(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_asset_ticker_histories_id'), 'asset_ticker_histories', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_asset_ticker_histories_id'), table_name='asset_ticker_histories')
    op.drop_table('asset_ticker_histories')

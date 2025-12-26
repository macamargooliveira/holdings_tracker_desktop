"""create assets

Revision ID: 84fc8bf13efc
Revises: c08d1e9fb28f
Create Date: 2025-12-26 14:28:00.732847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84fc8bf13efc'
down_revision: Union[str, Sequence[str], None] = 'c08d1e9fb28f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('assets',
    sa.Column('ticker', sa.String(length=12), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('sector_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
    sa.ForeignKeyConstraint(['sector_id'], ['asset_sectors.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['asset_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ticker')
    )
    op.create_index(op.f('ix_assets_id'), 'assets', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_assets_id'), table_name='assets')
    op.drop_table('assets')

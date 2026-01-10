"""create assets

Revision ID: 006
Revises: 005
Create Date: 2026-01-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '006'
down_revision: Union[str, Sequence[str], None] = '005'
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

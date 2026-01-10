"""create asset sectors

Revision ID: 005
Revises: 004
Create Date: 2026-01-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '005'
down_revision: Union[str, Sequence[str], None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('asset_sectors',
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('asset_type_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['asset_type_id'], ['asset_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_asset_sectors_id'), 'asset_sectors', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_asset_sectors_id'), table_name='asset_sectors')
    op.drop_table('asset_sectors')

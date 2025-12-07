"""initial

Revision ID: 638496e9bb9d
Revises: 
Create Date: 2025-12-07 13:07:18.895408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '638496e9bb9d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('countries',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('currencies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('code', sa.String(length=3), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('symbol', sa.String(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('asset_types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('brokers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('asset_sectors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('asset_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['asset_type_id'], ['asset_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ticker', sa.String(length=5), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('sector_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
    sa.ForeignKeyConstraint(['sector_id'], ['asset_sectors.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['asset_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ticker')
    )
    op.create_table('asset_events',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('event_type', sa.Enum('AMORTIZATION', 'REVERSE_SPLIT', 'SPLIT', 'SUBSCRIPTION', name='asseteventtype'), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('quantity', sa.Numeric(precision=20, scale=6), nullable=True),
    sa.Column('price', sa.Numeric(precision=20, scale=6), nullable=True),
    sa.Column('factor', sa.Numeric(precision=10, scale=6), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('asset_ticker_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('old_ticker', sa.String(length=5), nullable=False),
    sa.Column('new_ticker', sa.String(length=5), nullable=False),
    sa.Column('change_date', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('broker_notes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('operation', sa.Enum('BUY', 'SELL', name='operationtype'), nullable=False),
    sa.Column('broker_id', sa.Integer(), nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('price', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('fees', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('taxes', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('note_number', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.ForeignKeyConstraint(['broker_id'], ['brokers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('position_snapshots',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('quantity', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('avg_price', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.Column('total_invested', sa.Numeric(precision=20, scale=6), nullable=False),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('position_snapshots')
    op.drop_table('broker_notes')
    op.drop_table('asset_ticker_history')
    op.drop_table('asset_events')
    op.drop_table('assets')
    op.drop_table('asset_sectors')
    op.drop_table('brokers')
    op.drop_table('asset_types')
    op.drop_table('currencies')
    op.drop_table('countries')
    # ### end Alembic commands ###

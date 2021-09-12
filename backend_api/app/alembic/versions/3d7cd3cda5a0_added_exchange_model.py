"""Added Exchange model

Revision ID: 3d7cd3cda5a0
Revises: 00a37a693ca5
Create Date: 2021-09-07 01:32:59.746873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d7cd3cda5a0'
down_revision = '00a37a693ca5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exchange',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('supported_pairs', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exchange_id'), 'exchange', ['id'], unique=False)
    op.create_index(op.f('ix_exchange_name'), 'exchange', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_exchange_name'), table_name='exchange')
    op.drop_index(op.f('ix_exchange_id'), table_name='exchange')
    op.drop_table('exchange')
    # ### end Alembic commands ###
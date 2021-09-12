"""Added UserExchange model

Revision ID: 8a5ef916e5ba
Revises: a93c2c720d34
Create Date: 2021-09-07 02:02:58.326752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a5ef916e5ba'
down_revision = 'a93c2c720d34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_userexchange_exchange_id'), 'userexchange', ['exchange_id'], unique=False)
    op.create_index(op.f('ix_userexchange_user_id'), 'userexchange', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_userexchange_user_id'), table_name='userexchange')
    op.drop_index(op.f('ix_userexchange_exchange_id'), table_name='userexchange')
    # ### end Alembic commands ###
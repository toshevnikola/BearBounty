"""in_deal field in dcabot

Revision ID: 5e8ef5521d01
Revises: 960b749ae421
Create Date: 2021-10-01 01:38:20.537692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e8ef5521d01'
down_revision = '960b749ae421'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dcabot', sa.Column('in_deal', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dcabot', 'in_deal')
    # ### end Alembic commands ###
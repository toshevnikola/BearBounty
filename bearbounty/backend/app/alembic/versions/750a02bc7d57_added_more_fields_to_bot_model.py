"""Added more fields to Bot model

Revision ID: 750a02bc7d57
Revises: 6bf09e19ad93
Create Date: 2021-07-02 23:24:55.001432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '750a02bc7d57'
down_revision = '6bf09e19ad93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bot', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('bot', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bot', 'updated_at')
    op.drop_column('bot', 'created_at')
    # ### end Alembic commands ###

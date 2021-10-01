"""is_active field in Deal

Revision ID: 960b749ae421
Revises: 66f87ef3620a
Create Date: 2021-09-25 19:50:40.035728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "960b749ae421"
down_revision = "66f87ef3620a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("deal", sa.Column("is_active", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("deal", "is_active")
    # ### end Alembic commands ###

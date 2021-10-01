"""Added order model

Revision ID: 5fec6a652cd7
Revises: ff28fd837777
Create Date: 2021-09-12 15:06:22.681935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5fec6a652cd7"
down_revision = "ff28fd837777"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "deal",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bot_id", sa.Integer(), nullable=True),
        sa.Column("pair", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["bot_id"],
            ["dcabot.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_deal_bot_id"), "deal", ["bot_id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_deal_bot_id"), table_name="deal")
    op.drop_table("deal")
    # ### end Alembic commands ###
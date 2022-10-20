"""First migration

Revision ID: 20faf9aaf90f
Revises: 
Create Date: 2021-10-23 14:08:49.183445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20faf9aaf90f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "exchange",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("supported_pairs", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_exchange_id"), "exchange", ["id"], unique=False)
    op.create_index(op.f("ix_exchange_name"), "exchange", ["name"], unique=False)
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_first_name"), "user", ["first_name"], unique=False)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "userexchange",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("api_key", sa.String(), nullable=True),
        sa.Column("api_secret", sa.String(), nullable=True),
        sa.Column("balance", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("exchange_id", sa.Integer(), nullable=True),
        sa.Column("is_valid", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["exchange_id"],
            ["exchange.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_userexchange_exchange_id"),
        "userexchange",
        ["exchange_id"],
        unique=False,
    )
    op.create_index(op.f("ix_userexchange_id"), "userexchange", ["id"], unique=False)
    op.create_index(
        op.f("ix_userexchange_user_id"), "userexchange", ["user_id"], unique=False
    )
    op.create_table(
        "dcabot",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("required_balance", sa.Float(), nullable=True),
        sa.Column("base_coin", sa.String(), nullable=False),
        sa.Column("base_order_amount", sa.Float(), nullable=False),
        sa.Column("safety_order_amount", sa.Float(), nullable=False),
        sa.Column("max_safety_orders", sa.Integer(), nullable=False),
        sa.Column("max_active_safety_orders", sa.Integer(), nullable=False),
        sa.Column("safety_order_price_deviation_pct", sa.Float(), nullable=False),
        sa.Column("safety_order_price_deviation_scale", sa.Float(), nullable=False),
        sa.Column("allocated_funds", sa.Float(), nullable=True),
        sa.Column("trading_pairs", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("consider_overall_sentiment", sa.Boolean(), nullable=True),
        sa.Column("stop_loss_pct", sa.Float(), nullable=True),
        sa.Column("take_profit_pct", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_running", sa.Boolean(), nullable=True),
        sa.Column("in_deal", sa.Boolean(), nullable=True),
        sa.Column("avatar_color", sa.String(), nullable=True),
        sa.Column("user_exchange_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_exchange_id"],
            ["userexchange.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dcabot_id"), "dcabot", ["id"], unique=False)
    op.create_index(op.f("ix_dcabot_name"), "dcabot", ["name"], unique=False)
    op.create_index(
        op.f("ix_dcabot_user_exchange_id"), "dcabot", ["user_exchange_id"], unique=False
    )
    op.create_table(
        "deal",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bot_id", sa.Integer(), nullable=True),
        sa.Column("pair", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["bot_id"],
            ["dcabot.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_deal_bot_id"), "deal", ["bot_id"], unique=False)
    op.create_table(
        "order",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("deal_id", sa.Integer(), nullable=True),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("fee", sa.Float(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("active", "completed", "canceled", name="orderstatusenum"),
            nullable=True,
        ),
        sa.Column("type", sa.Enum("buy", "sell", name="ordertypeenum"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["deal_id"],
            ["deal.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_deal_id"), "order", ["deal_id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_order_deal_id"), table_name="order")
    op.drop_table("order")
    op.drop_index(op.f("ix_deal_bot_id"), table_name="deal")
    op.drop_table("deal")
    op.drop_index(op.f("ix_dcabot_user_exchange_id"), table_name="dcabot")
    op.drop_index(op.f("ix_dcabot_name"), table_name="dcabot")
    op.drop_index(op.f("ix_dcabot_id"), table_name="dcabot")
    op.drop_table("dcabot")
    op.drop_index(op.f("ix_userexchange_user_id"), table_name="userexchange")
    op.drop_index(op.f("ix_userexchange_id"), table_name="userexchange")
    op.drop_index(op.f("ix_userexchange_exchange_id"), table_name="userexchange")
    op.drop_table("userexchange")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_first_name"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_exchange_name"), table_name="exchange")
    op.drop_index(op.f("ix_exchange_id"), table_name="exchange")
    op.drop_table("exchange")
    # ### end Alembic commands ###
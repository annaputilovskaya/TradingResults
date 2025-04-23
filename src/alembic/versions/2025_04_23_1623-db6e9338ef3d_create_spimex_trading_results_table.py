"""Create spimex_trading_results table

Revision ID: db6e9338ef3d
Revises:
Create Date: 2025-04-23 16:23:35.845296

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "db6e9338ef3d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "spimex_trading_results",
        sa.Column("exchange_product_id", sa.String(length=11), nullable=False),
        sa.Column(
            "exchange_product_name", sa.String(length=255), nullable=False
        ),
        sa.Column("oil_id", sa.String(length=4), nullable=False),
        sa.Column("delivery_basis_id", sa.String(length=3), nullable=False),
        sa.Column(
            "delivery_basis_name", sa.String(length=255), nullable=False
        ),
        sa.Column("delivery_type_id", sa.String(length=1), nullable=False),
        sa.Column("volume", sa.Integer(), nullable=False),
        sa.Column("total", sa.Integer(), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.Column("date", sa.String(length=8), nullable=False),
        sa.Column(
            "created_on",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_on",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "exchange_product_id", "date", name="exchange_product_id_date"
        ),
    )
    op.create_index(
        op.f("ix_spimex_trading_results_date"),
        "spimex_trading_results",
        ["date"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_spimex_trading_results_date"),
        table_name="spimex_trading_results",
    )
    op.drop_table("spimex_trading_results")

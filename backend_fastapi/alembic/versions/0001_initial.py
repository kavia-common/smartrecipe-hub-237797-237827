"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-03-05

"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False, server_default="user"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("ingredients", sa.Text(), nullable=False),
        sa.Column("instructions", sa.Text(), nullable=False),
        sa.Column("cooking_time_minutes", sa.Integer(), nullable=False, server_default="15"),
        sa.Column("difficulty", sa.String(length=20), nullable=False, server_default="easy"),
        sa.Column("category", sa.String(length=80), nullable=False, server_default="general"),
        sa.Column("dietary_tags", sa.String(length=200), nullable=False, server_default=""),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_recipes_author_id", "recipes", ["author_id"])
    op.create_index("ix_recipes_title", "recipes", ["title"])

    op.create_table(
        "favorites",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("recipe_id", sa.Integer(), sa.ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "shopping_lists",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False, server_default="My Shopping List"),
        sa.Column("items", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_shopping_lists_user_id", "shopping_lists", ["user_id"])

    op.create_table(
        "meal_plans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("plan_date", sa.Date(), nullable=False),
        sa.Column("meal_type", sa.String(length=30), nullable=False, server_default="dinner"),
        sa.Column("recipe_id", sa.Integer(), sa.ForeignKey("recipes.id", ondelete="SET NULL"), nullable=True),
        sa.Column("note", sa.String(length=300), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_meal_plans_user_id", "meal_plans", ["user_id"])
    op.create_index("ix_meal_plans_plan_date", "meal_plans", ["plan_date"])


def downgrade() -> None:
    op.drop_index("ix_meal_plans_plan_date", table_name="meal_plans")
    op.drop_index("ix_meal_plans_user_id", table_name="meal_plans")
    op.drop_table("meal_plans")

    op.drop_index("ix_shopping_lists_user_id", table_name="shopping_lists")
    op.drop_table("shopping_lists")

    op.drop_table("favorites")

    op.drop_index("ix_recipes_title", table_name="recipes")
    op.drop_index("ix_recipes_author_id", table_name="recipes")
    op.drop_table("recipes")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

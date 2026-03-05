from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class ShoppingList(Base):
    """Shopping list generated/maintained by a user."""

    __tablename__ = "shopping_lists"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False, default="My Shopping List")
    items: Mapped[str] = mapped_column(Text, nullable=False, default="")  # newline-separated
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship("User", back_populates="shopping_lists")


class MealPlan(Base):
    """Meal plan entry for a given date (and optional recipe)."""

    __tablename__ = "meal_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    plan_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    meal_type: Mapped[str] = mapped_column(String(30), nullable=False, default="dinner")

    recipe_id: Mapped[int | None] = mapped_column(
        ForeignKey("recipes.id", ondelete="SET NULL"), nullable=True
    )
    note: Mapped[str] = mapped_column(String(300), nullable=False, default="")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user = relationship("User", back_populates="meal_plans")
    recipe = relationship("Recipe")

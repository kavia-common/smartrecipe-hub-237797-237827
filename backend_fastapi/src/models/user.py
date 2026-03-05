from datetime import datetime
from typing import Literal

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


UserRole = Literal["user", "admin"]


class User(Base):
    """Application user."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    recipes = relationship("Recipe", back_populates="author", cascade="all,delete")
    favorites = relationship("Favorite", back_populates="user", cascade="all,delete")
    shopping_lists = relationship("ShoppingList", back_populates="user", cascade="all,delete")
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all,delete")

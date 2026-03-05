from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Recipe(Base):
    """Recipe entity created by a user."""

    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    title: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ingredients: Mapped[str] = mapped_column(Text, nullable=False)
    instructions: Mapped[str] = mapped_column(Text, nullable=False)

    cooking_time_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False, default="easy")
    category: Mapped[str] = mapped_column(String(80), nullable=False, default="general")
    dietary_tags: Mapped[str] = mapped_column(String(200), nullable=False, default="")  # CSV tags
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    author = relationship("User", back_populates="recipes")
    favorited_by = relationship("Favorite", back_populates="recipe", cascade="all,delete")


class Favorite(Base):
    """User favorite recipe join table."""

    __tablename__ = "favorites"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user = relationship("User", back_populates="favorites")
    recipe = relationship("Recipe", back_populates="favorited_by")

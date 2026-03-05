"""Seed initial data.

Run (from backend_fastapi container root, with env configured):
  source venv/bin/activate
  python -m src.seed
"""
from sqlalchemy import select

from src.core.db import SessionLocal
from src.core.security import hash_password
from src.models import Recipe, User


def _ensure_user(db, *, name: str, email: str, password: str, role: str) -> User:
    user = db.scalar(select(User).where(User.email == email))
    if user:
        return user
    user = User(name=name, email=email, password_hash=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _ensure_recipe(db, *, author_id: int, title: str, **kwargs) -> Recipe:
    existing = db.scalar(select(Recipe).where(Recipe.author_id == author_id, Recipe.title == title))
    if existing:
        return existing
    recipe = Recipe(author_id=author_id, title=title, **kwargs)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


# PUBLIC_INTERFACE
def run_seed() -> None:
    """Seed database with an admin user and a few sample recipes."""
    db = SessionLocal()
    try:
        admin = _ensure_user(
            db,
            name="Admin",
            email="admin@smartrecipehub.local",
            password="admin123",
            role="admin",
        )
        demo = _ensure_user(
            db,
            name="Demo User",
            email="demo@smartrecipehub.local",
            password="demo1234",
            role="user",
        )

        _ensure_recipe(
            db,
            author_id=demo.id,
            title="Retro Tomato Toast",
            description="A quick snack with a nostalgic diner vibe.",
            ingredients="Bread slices\nTomato\nOlive oil\nSalt\nPepper\nOptional: basil",
            instructions="1) Toast bread.\n2) Rub with tomato.\n3) Drizzle olive oil.\n4) Season and serve.",
            cooking_time_minutes=10,
            difficulty="easy",
            category="snacks",
            dietary_tags="vegetarian",
            image_url=None,
        )

        _ensure_recipe(
            db,
            author_id=demo.id,
            title="Green Arcade Salad",
            description="Crunchy, bright, and pixel-perfect.",
            ingredients="Lettuce\nCucumber\nGreen apple\nPumpkin seeds\nLime juice\nSalt",
            instructions="1) Chop.\n2) Toss.\n3) Crunch loudly.",
            cooking_time_minutes=12,
            difficulty="easy",
            category="salads",
            dietary_tags="vegan,gluten-free",
            image_url=None,
        )

        print(f"Seed complete. Admin: {admin.email} / admin123")
        print(f"Seed complete. Demo: {demo.email} / demo1234")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()

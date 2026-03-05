from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.core.db import get_db
from src.models import Favorite, Recipe, User
from src.schemas.recipe import RecipePublic

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.get(
    "",
    response_model=list[RecipePublic],
    summary="List my favorite recipes",
    operation_id="favorites_list",
)
def list_favorites(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[RecipePublic]:
    """Return recipes favorited by current user."""
    stmt = (
        select(Recipe)
        .join(Favorite, Favorite.recipe_id == Recipe.id)
        .where(Favorite.user_id == user.id)
        .order_by(Favorite.created_at.desc())
    )
    return list(db.scalars(stmt).all())

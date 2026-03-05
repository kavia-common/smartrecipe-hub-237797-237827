from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.deps import require_admin
from src.core.db import get_db
from src.models import Recipe, User
from src.schemas.recipe import RecipePublic
from src.schemas.user import UserPublic

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get(
    "/users",
    response_model=list[UserPublic],
    summary="List users (admin)",
    operation_id="admin_list_users",
)
def list_users(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[UserPublic]:
    """List all users (admin-only)."""
    return list(db.scalars(select(User).order_by(User.created_at.desc())).all())


@router.get(
    "/recipes",
    response_model=list[RecipePublic],
    summary="List recipes (admin)",
    operation_id="admin_list_recipes",
)
def list_recipes(_: User = Depends(require_admin), db: Session = Depends(get_db)) -> list[RecipePublic]:
    """List all recipes (admin-only)."""
    return list(db.scalars(select(Recipe).order_by(Recipe.created_at.desc())).all())


@router.delete(
    "/recipes/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete any recipe (admin)",
    operation_id="admin_delete_recipe",
)
def delete_any_recipe(
    recipe_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> None:
    """Admin delete for moderation."""
    recipe = db.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
    return None

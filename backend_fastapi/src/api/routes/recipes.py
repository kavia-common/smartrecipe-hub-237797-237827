from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.core.db import get_db
from src.models import Favorite, Recipe, User
from src.schemas.recipe import RecipeCreate, RecipePublic, RecipeUpdate

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get(
    "",
    response_model=list[RecipePublic],
    summary="List recipes",
    description="Browse recipes. Supports simple search by title/ingredients/category/tags.",
    operation_id="recipes_list",
)
def list_recipes(
    q: str | None = Query(None, description="Search query (title/ingredients/category/tags)"),
    category: str | None = Query(None, description="Filter by category"),
    tag: str | None = Query(None, description="Filter by dietary tag (matches CSV)"),
    db: Session = Depends(get_db),
) -> list[RecipePublic]:
    """List recipes with optional search and filters."""
    stmt = select(Recipe).order_by(Recipe.created_at.desc())
    if q:
        like = f"%{q.lower()}%"
        stmt = stmt.where(
            or_(
                Recipe.title.ilike(like),
                Recipe.ingredients.ilike(like),
                Recipe.category.ilike(like),
                Recipe.dietary_tags.ilike(like),
            )
        )
    if category:
        stmt = stmt.where(Recipe.category == category)
    if tag:
        stmt = stmt.where(Recipe.dietary_tags.ilike(f"%{tag}%"))
    return list(db.scalars(stmt).all())


@router.get(
    "/{recipe_id}",
    response_model=RecipePublic,
    summary="Get recipe details",
    operation_id="recipes_get",
)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)) -> RecipePublic:
    """Fetch a single recipe."""
    recipe = db.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post(
    "",
    response_model=RecipePublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create recipe",
    description="Authenticated users can create recipes.",
    operation_id="recipes_create",
)
def create_recipe(
    payload: RecipeCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RecipePublic:
    """Create a new recipe."""
    recipe = Recipe(author_id=user.id, **payload.model_dump())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.patch(
    "/{recipe_id}",
    response_model=RecipePublic,
    summary="Update recipe",
    description="Only the recipe author or an admin can update a recipe.",
    operation_id="recipes_update",
)
def update_recipe(
    recipe_id: int,
    payload: RecipeUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RecipePublic:
    """Update a recipe."""
    recipe = db.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe.author_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not permitted")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(recipe, k, v)

    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete recipe",
    description="Only the recipe author or an admin can delete a recipe.",
    operation_id="recipes_delete",
)
def delete_recipe(
    recipe_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete a recipe."""
    recipe = db.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe.author_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not permitted")

    db.delete(recipe)
    db.commit()
    return None


@router.post(
    "/{recipe_id}/favorite",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Favorite a recipe",
    operation_id="recipes_favorite",
)
def favorite_recipe(
    recipe_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Mark a recipe as a favorite for current user."""
    recipe = db.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    existing = db.get(Favorite, {"user_id": user.id, "recipe_id": recipe_id})
    if existing:
        return None

    db.add(Favorite(user_id=user.id, recipe_id=recipe_id))
    db.commit()
    return None


@router.delete(
    "/{recipe_id}/favorite",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unfavorite a recipe",
    operation_id="recipes_unfavorite",
)
def unfavorite_recipe(
    recipe_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Remove a recipe from favorites."""
    fav = db.get(Favorite, {"user_id": user.id, "recipe_id": recipe_id})
    if fav:
        db.delete(fav)
        db.commit()
    return None

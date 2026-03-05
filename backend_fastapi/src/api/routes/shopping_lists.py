from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.core.db import get_db
from src.models import ShoppingList, User
from src.schemas.planning import ShoppingListCreate, ShoppingListPublic

router = APIRouter(prefix="/shopping-lists", tags=["Shopping Lists"])


@router.get(
    "",
    response_model=list[ShoppingListPublic],
    summary="List my shopping lists",
    operation_id="shopping_lists_list",
)
def list_lists(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ShoppingListPublic]:
    """List shopping lists for the current user."""
    stmt = select(ShoppingList).where(ShoppingList.user_id == user.id).order_by(ShoppingList.updated_at.desc())
    return list(db.scalars(stmt).all())


@router.post(
    "",
    response_model=ShoppingListPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create shopping list",
    operation_id="shopping_lists_create",
)
def create_list(
    payload: ShoppingListCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ShoppingListPublic:
    """Create a new shopping list."""
    item = ShoppingList(user_id=user.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch(
    "/{list_id}",
    response_model=ShoppingListPublic,
    summary="Update shopping list",
    operation_id="shopping_lists_update",
)
def update_list(
    list_id: int,
    payload: ShoppingListCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ShoppingListPublic:
    """Update a shopping list."""
    item = db.get(ShoppingList, list_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Shopping list not found")

    item.title = payload.title
    item.items = payload.items
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete(
    "/{list_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete shopping list",
    operation_id="shopping_lists_delete",
)
def delete_list(
    list_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete a shopping list."""
    item = db.get(ShoppingList, list_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    db.delete(item)
    db.commit()
    return None

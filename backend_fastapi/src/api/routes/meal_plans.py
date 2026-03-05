from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.core.db import get_db
from src.models import MealPlan, User
from src.schemas.planning import MealPlanCreate, MealPlanPublic

router = APIRouter(prefix="/meal-plans", tags=["Meal Plans"])


@router.get(
    "",
    response_model=list[MealPlanPublic],
    summary="List my meal plans",
    description="Optionally filter by date range.",
    operation_id="meal_plans_list",
)
def list_meal_plans(
    start: date | None = Query(None, description="Start date"),
    end: date | None = Query(None, description="End date"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[MealPlanPublic]:
    """List meal plans for current user."""
    stmt = select(MealPlan).where(MealPlan.user_id == user.id).order_by(MealPlan.plan_date.asc())
    if start:
        stmt = stmt.where(MealPlan.plan_date >= start)
    if end:
        stmt = stmt.where(MealPlan.plan_date <= end)
    return list(db.scalars(stmt).all())


@router.post(
    "",
    response_model=MealPlanPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create meal plan entry",
    operation_id="meal_plans_create",
)
def create_meal_plan(
    payload: MealPlanCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MealPlanPublic:
    """Create a meal plan entry."""
    item = MealPlan(user_id=user.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete(
    "/{meal_plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete meal plan entry",
    operation_id="meal_plans_delete",
)
def delete_meal_plan(
    meal_plan_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete a meal plan entry."""
    item = db.get(MealPlan, meal_plan_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Meal plan entry not found")
    db.delete(item)
    db.commit()
    return None

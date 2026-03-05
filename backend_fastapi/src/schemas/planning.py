from datetime import date, datetime

from pydantic import BaseModel, Field


class ShoppingListCreate(BaseModel):
    title: str = Field("My Shopping List", max_length=200, description="Shopping list title")
    items: str = Field("", description="Newline-separated list items")


class ShoppingListPublic(BaseModel):
    id: int = Field(..., description="Shopping list id")
    user_id: int = Field(..., description="Owner user id")
    title: str = Field(..., description="Title")
    items: str = Field(..., description="Items")
    created_at: datetime = Field(..., description="Created at")
    updated_at: datetime = Field(..., description="Updated at")

    class Config:
        from_attributes = True


class MealPlanCreate(BaseModel):
    plan_date: date = Field(..., description="Date for the meal plan entry")
    meal_type: str = Field("dinner", description="breakfast|lunch|dinner|snack")
    recipe_id: int | None = Field(None, description="Optional recipe id")
    note: str = Field("", max_length=300, description="Optional note")


class MealPlanPublic(BaseModel):
    id: int = Field(..., description="Meal plan id")
    user_id: int = Field(..., description="Owner user id")
    plan_date: date = Field(..., description="Date")
    meal_type: str = Field(..., description="Meal type")
    recipe_id: int | None = Field(None, description="Recipe id")
    note: str = Field(..., description="Note")
    created_at: datetime = Field(..., description="Created at")

    class Config:
        from_attributes = True

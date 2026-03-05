from datetime import datetime

from pydantic import BaseModel, Field


class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Recipe title")
    description: str | None = Field(None, max_length=500, description="Short description")
    ingredients: str = Field(..., min_length=1, description="Ingredients (free text)")
    instructions: str = Field(..., min_length=1, description="Steps/instructions (free text)")
    cooking_time_minutes: int = Field(15, ge=1, le=24 * 60, description="Cooking time in minutes")
    difficulty: str = Field("easy", description="easy|medium|hard")
    category: str = Field("general", max_length=80, description="Recipe category")
    dietary_tags: str = Field("", max_length=200, description="CSV dietary tags, e.g. vegan,gluten-free")
    image_url: str | None = Field(None, max_length=500, description="Optional image URL")


class RecipeUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=500)
    ingredients: str | None = Field(None, min_length=1)
    instructions: str | None = Field(None, min_length=1)
    cooking_time_minutes: int | None = Field(None, ge=1, le=24 * 60)
    difficulty: str | None = Field(None)
    category: str | None = Field(None, max_length=80)
    dietary_tags: str | None = Field(None, max_length=200)
    image_url: str | None = Field(None, max_length=500)


class RecipePublic(BaseModel):
    id: int = Field(..., description="Recipe id")
    author_id: int = Field(..., description="Author user id")
    title: str = Field(..., description="Recipe title")
    description: str | None = Field(None, description="Short description")
    ingredients: str = Field(..., description="Ingredients")
    instructions: str = Field(..., description="Instructions")
    cooking_time_minutes: int = Field(..., description="Cooking time in minutes")
    difficulty: str = Field(..., description="Difficulty")
    category: str = Field(..., description="Category")
    dietary_tags: str = Field(..., description="CSV dietary tags")
    image_url: str | None = Field(None, description="Image URL")
    created_at: datetime = Field(..., description="Created timestamp")
    updated_at: datetime = Field(..., description="Updated timestamp")

    class Config:
        from_attributes = True

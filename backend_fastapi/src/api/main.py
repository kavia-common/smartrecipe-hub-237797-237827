from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import admin, auth, favorites, meal_plans, recipes, shopping_lists
from src.core.config import settings

openapi_tags = [
    {"name": "Auth", "description": "User registration and JWT authentication."},
    {"name": "Recipes", "description": "Browse, search, create, and manage recipes."},
    {"name": "Favorites", "description": "Save and manage favorite recipes."},
    {"name": "Shopping Lists", "description": "Create and manage shopping lists."},
    {"name": "Meal Plans", "description": "Meal planning calendar endpoints."},
    {"name": "Admin", "description": "Admin-only moderation and management endpoints."},
]

app = FastAPI(
    title="SmartRecipe Hub API",
    description=(
        "Backend for SmartRecipe Hub. Provides JWT-based authentication and "
        "role-based access for recipe management, favorites, shopping lists, and meal planning."
    ),
    version="0.1.0",
    openapi_tags=openapi_tags,
)

cors_origins_raw = (
    settings.CORS_ORIGINS
    or settings.ALLOWED_ORIGINS
    or settings.CORS_ALLOW_ORIGINS
    or ""
)
allow_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]
if not allow_origins:
    allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    summary="Health check",
    description="Simple health check endpoint.",
    tags=["Auth"],
    operation_id="health_check",
)
def health_check():
    """Health check endpoint.

    Returns:
        JSON message confirming service is up.
    """
    return {"message": "Healthy"}


app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(favorites.router)
app.include_router(shopping_lists.router)
app.include_router(meal_plans.router)
app.include_router(admin.router)

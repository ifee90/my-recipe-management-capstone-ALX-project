# recipes/urls.py
from django.urls import path
from .views import (
    RecipeListCreateView,
    RecipeDetailView,
    IngredientListCreateView,
    IngredientDetailView,
)

urlpatterns = [
    # -----------------------------
    # Recipe Endpoints
    # -----------------------------
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),

    # -----------------------------
    # Ingredient Endpoints
    # -----------------------------
    path('ingredients/', IngredientListCreateView.as_view(), name='ingredient-list-create'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient-detail'),
]

from django.urls import path
from .views import (
    RecipeListCreateView,
    RecipeDetailView,
    IngredientListCreateView,
    IngredientDetailView,
)

urlpatterns = [
    # -----------------------------
    # API Endpoints
    # -----------------------------
    path('recipes/', RecipeListCreateView.as_view(), name='api-recipe-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='api-recipe-detail'),
    path('ingredients/', IngredientListCreateView.as_view(), name='api-ingredient-list'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='api-ingredient-detail'),
]

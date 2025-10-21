from django.urls import path
from .views import RecipeListCreateView, RecipeDetailView

urlpatterns = [
    # -----------------------------
    # API Endpoints
    # -----------------------------
    path('recipes/', RecipeListCreateView.as_view(), name='api-recipe-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='api-recipe-detail'),
]

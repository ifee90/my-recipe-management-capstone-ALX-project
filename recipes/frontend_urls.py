from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # -----------------------------
    # Frontend Views
    # -----------------------------
    path('', views.recipe_list, name='recipe-list'),
    path('recipe/new/', views.recipe_form, name='recipe-create'),
    path('recipe/<int:pk>/edit/', views.recipe_form, name='recipe-edit'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe-delete'),
    path('ingredient/new/', views.ingredient_form, name='ingredient-create'),

    # -----------------------------
    # Authentication Views
    # -----------------------------
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='recipe-list'), name='logout'),
]

# recipe_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recipes.urls')),          # For your recipe endpoints
    path('api-auth/', include('rest_framework.urls')),  # 👈🏽 Enables DRF login/logout
]

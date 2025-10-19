from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API
    path('api/', include('recipes.urls')),  # Only API endpoints

    # Frontend + Auth
    path('', include('recipes.frontend_urls')),  # Homepage + all frontend/auth routes
]

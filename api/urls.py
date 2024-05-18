"""
URL Configuration for all API endpoints.
"""

from django.urls import path, include

urlpatterns = [
    path('api/user/', include('users.urls')),
    path('api/categories/', include('categories.urls')),
]

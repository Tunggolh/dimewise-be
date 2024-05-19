"""
URL mapping for categories app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from categories.views import CategoryViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet)

app_name = 'categories'

urlpatterns = [
    path('', include(router.urls))
]

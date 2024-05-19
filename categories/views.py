"""
Views for the categories app.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Manage categories in the database
    """
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return appropriate serializer class
        """
        if self.action == 'list':
            return CategorySerializer

        return self.serializer_class

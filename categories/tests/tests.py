"""
Tests for categories API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from categories.models import Category
from categories.serializers import CategorySerializer

CATEGORIES_URL = reverse('categories:category-list')


def create_category(**params):
    """Create and return a category"""
    defaults = {
        'name': 'Test Category',
    }
    defaults.update(params)

    return Category.objects.create(**defaults)


class PublicCategoriesApiTests(TestCase):
    """Test the categories API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoriesApiTests(TestCase):
    """Test the categories API (private)"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='password123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_categories(self):
        """Test retrieving categories"""
        create_category()
        create_category()

        res = self.client.get(CATEGORIES_URL)

        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

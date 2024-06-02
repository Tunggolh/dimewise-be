"""
Tests for categories API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from transactions.models import Category
from transactions.serializers import CategorySerializer, CategoryDetailSerializer

CATEGORIES_URL = reverse('category-list')
CATEGORY_DETAIL_URL = 'category-detail'


def detail_category(category_id):
    """Return category detail URL"""
    return reverse(CATEGORY_DETAIL_URL, args=[category_id])


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

    def test_get_category_detail(self):
        """Test getting a category detail"""
        category = create_category()

        res = self.client.get(detail_category(category.id))

        serializer = CategoryDetailSerializer(category)
        self.assertEqual(res.data, serializer.data)

    def test_create_category(self):
        """Test creating a category"""
        payload = {'name': 'Test Category'}
        self.client.post(CATEGORIES_URL, payload)

        exists = Category.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_partial_update_category(self):
        """Test updating a category with patch"""
        category = create_category()
        payload = {'name': 'New Category'}

        self.client.patch(detail_category(category.id), payload)

        category.refresh_from_db()
        self.assertEqual(category.name, payload['name'])

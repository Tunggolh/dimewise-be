"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from categories.models import Category


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_category_successful(self):
        """Test creating a new category is successful"""
        category = Category.objects.create(
            name='Test Category'
        )

        self.assertEqual(category.name, 'Test Category')

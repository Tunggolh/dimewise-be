"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from categories.models import Category
from transactions.models import TransactionType, Transaction
from api.models import UserTransactionCategory


def create_user(email='test@example.com', password='testpass123'):
    """Create and return a user"""
    return get_user_model().objects.create_user(email, password)


def create_transaction_type(name='Income'):
    return TransactionType.objects.create(name=name)


def create_category(name='Salary'):
    return Category.objects.create(name=name)


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

    def test_create_user_transaction_category_successful(self):
        """Test creating a new user transaction category is successful"""
        user = create_user()
        transaction_type = create_transaction_type()
        category = create_category()

        user_transaction_category = UserTransactionCategory.objects.create(
            category=category,
            transaction_type=transaction_type,
            user=user
        )

        self.assertEqual(
            str(user_transaction_category),
            f'{transaction_type.name} - {category.name}'
        )

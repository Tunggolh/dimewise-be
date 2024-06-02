"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from transactions.models import (
    Category, TransactionType, Transaction, Account, AccountType)


def create_user(email='test@example.com', password='testpass123'):
    """Create and return a user"""
    return get_user_model().objects.create_user(email, password)


def create_transaction_type(name='Income'):
    return TransactionType.objects.create(name=name)


def create_category(name='Salary'):
    return Category.objects.create(name=name)


def create_account_type(name='Cash'):
    return AccountType.objects.create(name=name)


class ModelTests(TestCase):

    def test_create_category_successful(self):
        """Test creating a new category is successful"""
        category = Category.objects.create(
            name='Test Category'
        )

        self.assertEqual(category.name, 'Test Category')

    def test_create_transaction_type_successful(self):
        """Test creating a new transaction type is successful"""
        transaction_type = TransactionType.objects.create(
            name='Income'
        )

        self.assertEqual(transaction_type.name, 'Income')

    def test_create_account_type_successful(self):
        """Test creating a new account type is successful"""
        account_type = AccountType.objects.create(
            name='Cash'
        )

        self.assertEqual(account_type.name, 'Cash')

    def test_create_account_successful(self):
        """Test creating a new account is successful"""
        account_type = create_account_type()
        user = create_user()

        account = Account.objects.create(
            name='Cash',
            account_type=account_type,
            user=user,
            balance=0
        )

        self.assertEqual(account.name, 'Cash')

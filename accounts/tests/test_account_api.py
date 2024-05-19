"""
Tests for account and account type API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import Account, AccountType
from accounts.serializers import AccountSerializer, AccountDetailSerializer, AccountTypeSerializer, AccountTypeDetailSerializer

ACCOUNTS_URL = reverse('accounts:account-list')
ACCOUNT_DETAIL_URL = reverse('accounts:account-detail')
ACCOUNT_TYPES_URL = reverse('accounts:account-type-list')
ACCOUNT_TYPE_DETAIL_URL = reverse('accounts:account-type-detail')


def create_user(email='test@example.com', password='testpass123'):
    """Create and return a user"""
    return get_user_model().objects.create_user(email, password)


def create_superuser(email='admin@example.com', password='adminpass123'):
    """Create and return a superuser"""
    return get_user_model().objects.create_superuser(email, password)


def create_account_type(name='Cash'):
    return AccountType.objects.create(name=name)


def detail_account(account_id):
    """Return account detail URL"""
    return reverse(ACCOUNT_DETAIL_URL, args=[account_id])


def detail_account_type(account_type_id):
    """Return account type detail URL"""
    return reverse(ACCOUNT_TYPE_DETAIL_URL, args=[account_type_id])


class PublicAccountAndAccountTypeApiTests(TestCase):
    """Test the account and account type API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_account_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(ACCOUNTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_account_type_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(ACCOUNT_TYPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAccountTypeApiTests(TestCase):
    """Test the account type API (private)"""

    def setUp(self):
        self.user = create_superuser()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_account_types(self):
        """Test retrieving account types"""
        create_account_type()
        create_account_type("Credit Card")

        res = self.client.get(ACCOUNT_TYPES_URL)

        account_types = AccountType.objects.all().order_by('name')
        serializer = AccountTypeSerializer(account_types, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_account_type_detail(self):
        """Test getting an account type detail"""
        account_type = create_account_type()

        res = self.client.get(detail_account_type(account_type.id))

        serializer = AccountTypeDetailSerializer(account_type)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_account_type_unauthorized(self):
        """Test that an unauthorized user cannot create an account type"""
        self.user = create_user()

        payload = {
            'name': 'Savings'
        }

        res = self.client.post(ACCOUNT_TYPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_account_type_unauthorized(self):
        """Test that an unauthorized user cannot update an account type"""
        account_type = create_account_type()
        self.user = create_user()

        payload = {
            'name': 'Savings'
        }

        res = self.client.patch(detail_account_type(account_type.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_account_type_unauthorized(self):
        """Test that an unauthorized user cannot delete an account type"""
        account_type = create_account_type()
        self.user = create_user()

        res = self.client.delete(detail_account_type(account_type.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_account_type(self):
        """Test creating an account type"""
        payload = {
            'name': 'Savings'
        }

        res = self.client.post(ACCOUNT_TYPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = AccountType.objects.filter(
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_partial_update_account_type(self):
        """Test updating an account type with patch"""
        account_type = create_account_type()
        payload = {'name': 'Savings'}

        self.client.patch(detail_account_type(account_type.id), payload)

        account_type.refresh_from_db()
        self.assertEqual(account_type.name, payload['name'])

    def test_delete_account_type(self):
        """Test deleting an account type"""
        account_type = create_account_type()

        res = self.client.delete(detail_account_type(account_type.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = AccountType.objects.filter(id=account_type.id).exists()
        self.assertFalse(exists)


class PrivateAccountApiTests(TestCase):
    """Test the account API (private)"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.other_user = create_user(email='otheruser@example.com')

    def test_retrieve_accounts_specific_user(self):
        """Test retrieving accounts for specific user"""
        account_type_cash = create_account_type()
        account_type_savings = create_account_type("Savings")

        Account.objects.create(
            name='Piggy Bank',
            user=self.user,
            balance=1000,
            account_type=account_type_cash
        )

        Account.objects.create(
            name='Bank Account',
            user=self.user,
            balance=5000,
            account_type=account_type_savings
        )

        res = self.client.get(ACCOUNTS_URL)

        accounts = Account.objects.filter(user=self.user).order_by('name')
        serializer = AccountSerializer(accounts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_account(self):
        """Test creating an account"""
        account_type = create_account_type()

        payload = {
            'name': 'Piggy Bank',
            'account_type': account_type.id,
            'balance': 1000,
            'user': self.user.id
        }

        res = self.client.post(ACCOUNTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Account.objects.filter(
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_get_account_detail(self):
        """Test getting an account detail"""
        account_type = create_account_type()
        account = Account.objects.create(
            name='Piggy Bank',
            user=self.user,
            balance=1000,
            account_type=account_type
        )

        res = self.client.get(detail_account(account.id))

        serializer = AccountDetailSerializer(account)

        self.assertEqual(res.data, serializer.data)

    def test_partial_update_account_by_owner(self):
        """Test updating an account with patch"""
        account_type = create_account_type()
        account = Account.objects.create(
            name='Piggy Bank',
            user=self.user,
            balance=1000,
            account_type=account_type
        )

        payload = {'name': 'Bank Account'}

        self.client.patch(detail_account(account.id), payload)

        account.refresh_from_db()
        self.assertEqual(account.name, payload['name'])

    def test_delete_account_by_owner(self):
        """Test deleting an account"""
        account_type = create_account_type()
        account = Account.objects.create(
            name='Piggy Bank',
            user=self.user,
            balance=1000,
            account_type=account_type
        )

        res = self.client.delete(detail_account(account.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Account.objects.filter(id=account.id).exists()
        self.assertFalse(exists)

    def test_partial_update_account_by_other_user(self):
        """Test that an unauthorized user cannot update an account"""
        account_type = create_account_type()
        account = Account.objects.create(
            name='Piggy Bank',
            user=self.user,
            balance=1000,
            account_type=account_type
        )

        payload = {'name': 'Bank Account'}

        self.client.force_authenticate(self.other_user)

        res = self.client.patch(detail_account(account.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_account_by_other_user(self):
        """Test that an unauthorized user cannot delete an account"""
        account_type = create_account_type()
        account = Account.objects.create(
            name='Piggy Bank',
            user=self.user,
            balance=1000,
            account_type=account_type
        )

        self.client.force_authenticate(self.other_user)

        res = self.client.delete(detail_account(account.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

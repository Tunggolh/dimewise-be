"""
Tests for user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token_obtain_pair')
TOKEN_REFRESH_URL = reverse('users:token_refresh')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'user1@example.com',
            'password': 'testpass123',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test creating user that already exists fails"""
        payload = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'user1@example.com',
            'password': 'testpass123',
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'user2@example.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'test@example.com',
            'password': 'Admin123!'
        }

        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@example.com', password='password123')

        payload = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_email_password(self):
        """Test that token is not created if email or password is blank"""
        payload1 = {
            'email': '',
            'password': 'password123'
        }

        res = self.client.post(TOKEN_URL, payload1)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload2 = {
            'email': 'test@example.com',
            'password': ''
        }

        res = self.client.post(TOKEN_URL, payload2)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):
        """Test that a token can be refreshed"""
        create_user(email='test@example.com', password='password123')

        payload = {
            'email': 'test@example.com',
            'password': 'password123'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('refresh', res.data)
        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        refresh = res.data['refresh']
        refresh_payload = {
            'refresh': refresh
        }

        res = self.client.post(TOKEN_REFRESH_URL, refresh_payload)

        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_refresh_token_invalid(self):
        """Test that an invalid refresh token is rejected"""
        payload = {
            'refresh': 'invalid'
        }

        res = self.client.post(TOKEN_REFRESH_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

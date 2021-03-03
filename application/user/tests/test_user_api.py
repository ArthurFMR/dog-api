from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# URLs to test
CREATE_USER_URL = reverse('user:register')
AUTH_URL = reverse('user:auth')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test: Users API (PUBLIC)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test: Creating user with valid payload is successfuls"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'name': 'Test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_token_for_user(self):
        """Test: Create token for the user"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'password123'
        }
        create_user(**payload)
        res = self.client.post(AUTH_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test: token is not creted if invalid credentials are given"""

        create_user(email='test@gmail.com', password='password123')
        payload = {
            'email': 'test@gmail.com',
            'password': 'wrongpassword'
        }
        res = self.client.post(AUTH_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

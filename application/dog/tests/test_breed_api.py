from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Breed


BREEDS_URL = reverse('dog:breed-list')


class PublicBreedsApiTests(TestCase):
    """Test: Publicicly available breeds API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test: Login is required for retrieving breeds"""

        res = self.client.get(BREEDS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBreedsApiTests(TestCase):
    """Test: authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'user@gmail.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_breeds_with_pagination(self):
        """Test: retrieving breeds with pagination"""

        breeds = ['Chihuahua', 'Siberian Husky', 'German Shepherd',
                  'Bulldog', 'Labrador Retriever', 'French Bulldog',
                  'Bernese Mountain Dog', 'Pomeranian', 'Shih Tzu',
                  'Dobermann', 'Pomeranian']

        for breed in breeds:
            Breed.objects.create(name=breed)

        res = self.client.get(BREEDS_URL)

        self.assertIn('count', res.data.keys())
        self.assertIn('next', res.data.keys())
        self.assertIn('previous', res.data.keys())
        self.assertIn('results', res.data.keys())
        self.assertEqual(len(res.data['results']), 10)

    def test_retrieve_breed_by_name(self):
        """Test: Retrieving breed by name"""

        Breed.objects.create(name='Chihuahua')
        Breed.objects.create(name='Dobermann')

        res = self.client.get(BREEDS_URL + "?name=Chihuahua")

        breed = Breed.objects.get(name='Chihuahua')

        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['name'], breed.name)

    def test_create_breed_successful(self):
        """Test: Creating a New breed"""
        payload = {'name': 'Chihuahua'}
        self.client.post(BREEDS_URL, payload)

        exists = Breed.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

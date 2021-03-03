from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Dog, Breed

from dog.serializers import DogSerializer

DOGS_URL = reverse('dog:dog-list')


def sample_breed(name='Chihuahua'):
    """Create and return a sample breed"""
    return Breed.objects.create(name=name)


class PublicDogApiTests(TestCase):
    """Test: Unauthenticated Dog API Access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test: Authentication is required"""

        res = self.client.get(DOGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDogApiTests(TestCase):
    """Test: Authenticated recipe API Access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_dogs_with_pagination(self):
        """Test: Retrieving dogs with pagination"""
        dog_names = ['uffi', 'alti', 'piti', 'titi', 'fifi',
                     'rodolfo', 'bebe', 'tete', 'pipi',
                     'libi', 'tati']

        breed = sample_breed()

        for name in dog_names:
            Dog.objects.create(name=name, breed=breed)

        res = self.client.get(DOGS_URL)

        self.assertIn('count', res.data.keys())
        self.assertIn('next', res.data.keys())
        self.assertIn('previous', res.data.keys())
        self.assertIn('results', res.data.keys())
        self.assertIn('breed', res.data['results'][0].keys())
        self.assertEqual(len(res.data['results']), 5)

    def test_retrieve_dog_by_name(self):
        """Test: Retrieving dog by name"""
        breed = sample_breed(name='Doberman')

        Dog.objects.create(name='Firulai', breed=breed)
        Dog.objects.create(name='Firu', breed=breed)

        res = self.client.get(DOGS_URL + "?name=Firu")

        dog = Dog.objects.get(name='Firu')

        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['name'], dog.name)

    def test_retrieve_dogs_by_breed(self):
        """Test: Retrieving dogs by breed"""
        doberman = sample_breed(name='Doberman')
        chihuauha = sample_breed(name='Chihuahua')

        Dog.objects.create(name='Firulai', breed=doberman)
        Dog.objects.create(name='Firu', breed=doberman)
        Dog.objects.create(name='Uffi', breed=chihuauha)

        # res = self.client.get(DOGS_URL + "?breed=Doberman")
        res = self.client.get(DOGS_URL + "?breed_name=Doberman")

        dogs = Dog.objects.filter(breed=doberman).order_by('-id')
        serializer = DogSerializer(dogs, many=True)

        self.assertEqual(len(res.data['results']), 2)
        self.assertEqual(res.data['results'], serializer.data)

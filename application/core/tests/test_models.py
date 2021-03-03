from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test: creating new user with an email is succesful"""
        email = 'test@gmail.com'
        password = 'TestPassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_no_email(self):
        """Test: creating user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'pass123')

    def test_new_user_no_password(self):
        """Test: creating user with no password and raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@gmail.com', None)

    def test_create_new_superuser(self):
        """Test: creatomg a new superuser"""
        email = 'test@gmail.com'
        password = 'TestPassword123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)

    def test_breed_str(self):
        """Test: breed string representation"""

        breed = models.Breed.objects.create(
            name='Chihuahua'
        )

        self.assertEqual(str(breed), breed.name)

    def test_dog_str(self):
        """Test: Dog string representation"""

        dog = models.Dog.objects.create(
            name='Uffi',
            breed=models.Breed.objects.create(name='Chihuahua')
        )
        self.assertEqual(str(dog), dog.name)

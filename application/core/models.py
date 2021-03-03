from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Creates and saves a new user"""

        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Encrypt password

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Breed(models.Model):
    """Breed to be used for Dog"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Dog(models.Model):
    """Dog Object"""
    name = models.CharField(max_length=255)
    breed = models.ForeignKey(
        'Breed',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

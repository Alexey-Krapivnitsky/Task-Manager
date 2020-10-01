from django.contrib.auth.models import AbstractBaseUser
from django.db.models import EmailField, BooleanField

from authapp.managers import CustomUserManager


class User(AbstractBaseUser):
    username = EmailField(max_length=78, unique=True)
    is_active = BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

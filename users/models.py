from django.contrib.auth.models import AbstractUser
from django.db import models

from main.models import NULLABLE


class User (AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='почта',
        unique=True
    )

    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=10, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import AUTH_USER_MODEL
from mainapp.special_elements import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='электронная почта', help_text='обязательное поле')
    phone = models.CharField(max_length=50, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    token_verification = models.CharField(max_length=50, verbose_name='код верификации', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('can_block_user', 'Может заблокировать пользователя')
        ]


class Client(models.Model):
    email = models.EmailField(verbose_name='электронная почта', unique=True)
    first_name = models.CharField(max_length=50, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='фамилия', **NULLABLE)
    comment = models.CharField(max_length=400, **NULLABLE)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='отправитель', **NULLABLE)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


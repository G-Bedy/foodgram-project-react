from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    # is_subscribed = models.ManyToManyField('self', symmetrical=False, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    # Логин, пароль, email, имя и фамилия уже есть в AbstractUser
    # Задаем email как обязательное поле
    # is_staff уже существует в AbstractUser, мы можем использовать его для обозначения администраторов
    # По умолчанию значение False. Можно задать True для администраторов.
    # Имя и фамилия по умолчанию не обязательные, сделаем их обязательными


class Subscriber(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriber')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscription')

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"



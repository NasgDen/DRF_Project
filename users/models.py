from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """ Описание полей модель пользователь """

    email = models.EmailField(verbose_name="Почта", help_text="Введите почту")
    phone = models.CharField(max_length=15, verbose_name="Номер телефона", help_text="Введите номер телефона", blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name="Город", help_text="Введите город", blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatar/", blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

from symtable import Class

from django.conf import settings
from django.db import models

from users.models import User


class Course(models.Model):
    """Описание полей модель - курс"""

    name = models.CharField(max_length=100, verbose_name="Название", help_text="Введите название курса")
    image = models.ImageField(
        upload_to="media/", verbose_name="Превью", help_text="Загрузите картинку (превью)", blank=True, null=True
    )
    description = models.TextField(verbose_name="Описание курса", help_text="Введите описание курса")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        related_name="сourse",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Описание полей модель - урок"""

    name = models.CharField(max_length=100, verbose_name="Название", help_text="Введите название урока")
    description = models.TextField(verbose_name="Описание урока", help_text="Введите описание урока")
    image = models.ImageField(
        upload_to="media/", verbose_name="Превью", help_text="Загрузите картинку (превью)", blank=True, null=True
    )
    link_to_video = models.URLField(
        max_length=150, verbose_name="Ссылка на видео", help_text="Введите ссылку на видео", blank=True, null=True
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", help_text="Выберите курс", related_name="lesson"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        related_name="lesson",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name

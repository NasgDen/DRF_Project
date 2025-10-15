from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

PAYMENT_METHODS = [
    ("cash", "Наличные"),
    ("transfer", "Перевод на счет"),
]


class User(AbstractUser):
    """Описание полей модель пользователь"""

    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите почту")
    phone = models.CharField(
        max_length=15, verbose_name="Номер телефона", help_text="Введите номер телефона", blank=True, null=True
    )
    city = models.CharField(max_length=50, verbose_name="Город", help_text="Введите город", blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatar/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    """Описание полей модель платежи"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
        related_name="payment",
        blank=True,
        null=True
    )
    date_payment = models.DateField(verbose_name="Дата оплаты", auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Продукт")
    object_id = models.PositiveIntegerField(verbose_name="id Продукта")
    paid_item = GenericForeignKey("content_type", "object_id")
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS, verbose_name="Метод оплаты")
    amount = models.PositiveIntegerField(verbose_name="Стоимость")
    session_id = models.CharField(max_length=600, verbose_name="id сессии на оплату для stripe", blank=True, null=True)
    link =  models.CharField(max_length=600, verbose_name="Ссылка на оплату", blank=True, null=True)
    status = models.CharField(max_length=150, verbose_name="Статус оплаты", blank=True, null=True)

    class Meta:
        verbose_name = "Платежи"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} оплатил {self.amount} за {self.paid_item}  {self.date_payment}"

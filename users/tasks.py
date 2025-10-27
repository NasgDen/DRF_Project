from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_users_by_last_login_date():
    """Функция проверяет пользователей по дате последнего входа"""

    users = User.objects.all()
    current_time = timezone.now()
    for user in users:
        if user.last_login is not None:
            if current_time > user.last_login + timedelta(days=30):
                user.is_active = False
                user.save()
        else:
            if current_time > user.date_joined + timedelta(days=30):
                user.is_active = False
                user.save()

from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from lms.models import Subscription


@shared_task
def send_email_subscription(course, last_update_date):
    """Функция оправки письма пользователю при изменении курса"""

    subscription_courses = Subscription.objects.filter(course=course)
    user_list = []
    for subscription_course in subscription_courses:
        user_list.append(subscription_course.user)
        course_name = subscription_course.course.name
    time_delta = last_update_date + timedelta(hours=4)
    current_time = timezone.now()
    if user_list and current_time > time_delta:
        send_mail(f"Обновление курса {course_name}", f"Курс {course_name} обновился", EMAIL_HOST_USER, user_list)

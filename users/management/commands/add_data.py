from django.core.management import call_command
from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payments, User


class Command(BaseCommand):
    help = "Добавление данных в базу данных"

    def handle(self, *args, **kwargs):

        Course.objects.all().delete()
        Lesson.objects.all().delete()
        User.objects.all().delete()
        Payments.objects.all().delete()

        call_command("loaddata", "lms_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))

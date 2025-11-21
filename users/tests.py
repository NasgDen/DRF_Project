from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import Payments, User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", username="test")
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """Тест - создание пользователя"""
        url = reverse("users:user-list")
        data = {"email": "test2@mail.ru", "username": "test2"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_detail(self):
        """Тест - детальный просмотр курса"""
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

    def test_user_patch(self):
        """Тест - Изменение пользователя. Patch запрос"""
        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {"username": "admin"}
        response = self.client.patch(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("username"), "admin")

    def test_user_put(self):
        """Тест - Изменение пользователя. Put запрос"""
        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {
            "username": "admin",
            "email": "admin@mail.ru",
            "city": "M",
        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("email"), "admin@mail.ru")
        self.assertEqual(result.get("city"), "M")

    def test_user_delete(self):
        """Тест - Удаление пользователя."""
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)

    def test_user_list(self):
        """Тест - Вывод пользователей"""
        result = [
            {
                "username": self.user.username,
                "email": self.user.email,
                "city": self.user.city,
                "avatar": self.user.avatar,
            }
        ]
        url = reverse("users:user-list")
        group, created = Group.objects.get_or_create(name="moderators")
        user = self.user
        group.user_set.add(user)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


# class PaymentsTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create(email="test@mail.ru")
#         self.client.force_authenticate(user=self.user)
#         self.course = Course.objects.create(
#             name="Python", description="Изучение языка программирования Python", owner=self.user
#         )
#         self.lesson = Lesson.objects.create(
#             name="Переменные", description="Изучение переменных", course=self.course, owner=self.user
#         )
#         self.subscription = Subscription.objects.create(course=self.course, user=self.user)
#
#     def test_payments_list(self):
#         """Тест - Вывод платежей"""
#
#         payment = Payments(
#             user=self.user,
#             date_payment="2025-01-01",
#             content_type=ContentType.objects.get_for_model(self.course),
#             object_id=self.course.pk,
#             method="transfer",
#             amount=10000,
#         )
#         url = reverse("users:payments")
#         result = [
#             {
#                 "id": 1,
#                 "date_payment": payment.date_payment,
#                 "object_id": self.course.pk,
#                 "method": payment.method,
#                 "amount": payment.amount,
#                 "user": self.user.pk,
#                 "content_type": 6,
#             }
#         ]
#         response = self.client.get(url)
#         data = response.json()
#         print("resultat", result)
#         print("data:", data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data, result)

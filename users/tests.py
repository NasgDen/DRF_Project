from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group

from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", username="test")
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """ Тест - создание пользователя """
        url = reverse("users:user-list")
        data = {
            "email": "test2@mail.ru",
            "username": "test2"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            User.objects.all().count(),
            2
        )

    def test_user_detail(self):
        """ Тест - детальный просмотр курса """
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("email"),
            self.user.email
        )

    def test_user_patch(self):
        """ Тест - Изменение пользователя. Patch запрос"""
        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {
            "username": "admin"
        }
        response = self.client.patch(url, data)
        result = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            result.get("username"),
            "admin"
        )

    def test_user_put(self):
        """ Тест - Изменение пользователя. Put запрос"""
        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {
            "username": "admin",
            "email": "admin@mail.ru",
            "city": "M",

        }
        response = self.client.put(url, data)
        result = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            result.get("email"),
            "admin@mail.ru"
        )
        self.assertEqual(
            result.get("city"),
            "M"
        )

    def test_user_delete(self):
        """ Тест - Удаление пользователя. """
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            User.objects.all().count(),
            0
        )

    def test_user_list(self):
        """ Тест - Вывод пользователей """
        result = [
            {
                'username': self.user.username,
                'email': self.user.email,
                'city': self.user.city,
                'avatar': self.user.avatar
            }
        ]
        url = reverse("users:user-list")
        group, created = Group.objects.get_or_create(name="moderators")
        user = self.user
        group.user_set.add(user)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            result
        )
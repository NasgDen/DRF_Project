from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="Python", description="Изучение языка программирования Python", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Переменные", description="Изучение переменных", course=self.course, owner=self.user
        )

    def test_lesson_retrive(self):
        """Тест - детальный просмотр урока"""
        url = reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)
        self.assertEqual(data.get("description"), self.lesson.description)

    def test_lesson_create(self):
        """Тест - Создание урока"""
        url = reverse("lms:lesson_create")
        data = {"name": "Функции", "description": "Основы функций", "course": self.course.pk, "owner": self.user.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update_patch(self):
        """Тест - Изменение урока. Patch запрос"""
        url = reverse("lms:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Функция test",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update_put(self):
        """Тест - Изменение урока. Put запрос"""
        url = reverse("lms:lesson_update", args=(self.lesson.pk,))
        data = {"name": "Рекурсия", "description": "Основы функций", "course": self.course.pk, "owner": self.user.pk}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete(self):
        """Тест - Удаление урока."""
        url = reverse("lms:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест - Вывод уроков."""
        url = reverse("lms:lessons")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "image": self.lesson.image,
                    "link_to_video": self.lesson.link_to_video,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="Python", description="Изучение языка программирования Python", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Переменные", description="Изучение переменных", course=self.course, owner=self.user
        )

    def test_subscription_add(self):
        """Тест - Добавление подписки."""
        url = reverse("lms:subscription")
        data = {"course": self.course.pk, "user": self.user.pk}
        response = self.client.post(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("message"), "подписка добавлена")

    def test_subscription_delete(self):
        """Тест - Удаление подписки."""
        url = reverse("lms:subscription")
        Subscription.objects.create(course=self.course, user=self.user)
        data = {"course": self.course.pk, "user": self.user.pk}
        response = self.client.post(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("message"), "подписка удалена")


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="Python", description="Изучение языка программирования Python", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Переменные", description="Изучение переменных", course=self.course, owner=self.user
        )
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)

    def test_course_detail(self):
        """Тест - детальный просмотр курса"""
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        """Тест - создание курса"""
        url = reverse("lms:course-list")
        data = {
            "name": "test",
            "description": "test description",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    # def test_course_patch(self):
    #     """Тест - Изменение курса. Patch запрос"""
    #     url = reverse("lms:course-detail", args=(self.course.pk,))
    #     data = {"name": "test"}
    #     response = self.client.patch(url, data)
    #     result = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(result.get("name"), "test")

    # def test_course_put(self):
    #     """Тест - Изменение курса. Put запрос"""
    #     url = reverse("lms:course-detail", args=(self.course.pk,))
    #     data = {"name": "test", "description": "test description"}
    #     response = self.client.put(url, data)
    #     result = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(result.get("name"), "test")
    #     self.assertEqual(result.get("description"), "test description")

    def test_course_delete(self):
        """Тест - Удаление курса."""
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    # def test_course_list(self):
    #     """Тест - Вывод курсов"""
    #     url = reverse("lms:course-list")
    #     response = self.client.get(url)
    #     data = response.json()
    #     print("DATA: ", data)
    #     result = {
    #         "count": 1,
    #         "next": None,
    #         "previous": None,
    #         "results": [
    #             {
    #                 "id": self.course.pk,
    #                 "name": self.course.name,
    #                 "image": None,
    #                 "description": self.course.description,
    #                 "lessons": [
    #                     {
    #                         "id": self.lesson.pk,
    #                         "name": self.lesson.name,
    #                         "description": self.lesson.description,
    #                         "image": None,
    #                         "link_to_video": self.lesson.link_to_video,
    #                         "course": self.course.pk,
    #                         "owner": self.user.pk,
    #                     }
    #                 ],
    #                 "lessons_number": 1,
    #                 "owner": self.user.pk,
    #                 'last_update_date': self.course.last_update_date,
    #                 "subscription": True,
    #             }
    #         ],
    #     }
    #     print("DATA: ", data)
    #     print("RESULT: ", result)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data, result)

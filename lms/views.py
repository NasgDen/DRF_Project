from django.contrib.admin.templatetags.admin_list import pagination
from django.template.context_processors import request
from rest_framework import generics, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.permissions import IsModerator, IsOwner

from .models import Course, Lesson, Subscription
from .pagination import CoursePagination, LessonPagination
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .tasks import celery_test_work


class CourseViewSet(viewsets.ModelViewSet):
    """Класс реализует интерфейс для CRUD операция модели Course"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == "retrieve":
            self.permission_classes = [IsOwner | IsModerator]
        elif self.action == "update":
            self.permission_classes = [IsOwner | IsModerator]
        elif self.action == "partial_update":
            self.permission_classes = [IsOwner | IsModerator]
        elif self.action == "list":
            self.permission_classes = [IsModerator | IsAuthenticated]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        celery_test_work.delay(1, 2)
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        if IsModerator().has_permission(self.request, self):
            queryset = Course.objects.all()
        else:
            queryset = Course.objects.filter(owner=self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)


class LessonCreateApiView(generics.CreateAPIView):
    """Класс реализует интерфейс для создания урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonsListApiView(generics.ListAPIView):
    """Класс реализует интерфейс для создания урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            queryset = Lesson.objects.all()
        else:
            queryset = Lesson.objects.filter(owner=self.request.user)
        return queryset


class LessonUpdateApiView(generics.UpdateAPIView):
    """Класс реализует интерфейс для изменения урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonRetrieveApiView(generics.RetrieveAPIView):
    """Класс реализует интерфейс для отображения одного урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonsDestroyApiView(generics.DestroyAPIView):
    """Класс реализует интерфейс для удаления урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class SubscriptionApiView(APIView):
    """Класс реализует интерфейс для подписки на курсы"""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        return Response({"message": message})

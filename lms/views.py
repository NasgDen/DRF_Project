from rest_framework import generics, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lms.permissions import IsModerator, IsOwner

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Класс реализует интерфейс для CRUD операция модели Course"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        if IsModerator().has_permission(self.request, self):
            queryset = Course.objects.all()
        else:
            queryset = Course.objects.filter(owner=self.request.user)
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

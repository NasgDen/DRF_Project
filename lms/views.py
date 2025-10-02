from rest_framework import generics, viewsets

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Класс реализует интерфейс для CRUD операция модели Course"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateApiView(generics.CreateAPIView):
    """Класс реализует интерфейс для создания урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonsListApiView(generics.ListAPIView):
    """Класс реализует интерфейс для создания урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateApiView(generics.UpdateAPIView):
    """Класс реализует интерфейс для изменения урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveApiView(generics.RetrieveAPIView):
    """Класс реализует интерфейс для отображения одного урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonsDestroyApiView(generics.DestroyAPIView):
    """Класс реализует интерфейс для удаления урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

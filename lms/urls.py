from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import LmsConfig
from .views import (CourseViewSet, LessonCreateApiView, LessonRetrieveApiView, LessonsDestroyApiView,
                    LessonsListApiView, LessonUpdateApiView)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonsListApiView.as_view(), name="lessons"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson_update"),
    path("lessons/<int:pk>/delete/", LessonsDestroyApiView.as_view(), name="lesson_delete"),
] + router.urls

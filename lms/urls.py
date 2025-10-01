from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet
from .apps import LmsConfig

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'course',CourseViewSet, basename="course")

urlpatterns = [

] + router.urls
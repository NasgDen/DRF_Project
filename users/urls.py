from django.urls import path
from rest_framework import routers

from .apps import UsersConfig
from .views import PaymentsView, UserViewSet

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("payments/", PaymentsView.as_view(), name="payments"),
] + router.urls

from rest_framework import routers

from .apps import UsersConfig
from .views import UserViewSet

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [] + router.urls

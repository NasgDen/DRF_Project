from django.urls import path
from rest_framework import routers
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import PaymentsCreate, PaymentsUpdate, PaymentsView, UserViewSet

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("payments/", PaymentsView.as_view(), name="payments"),
    path("payments/create/", PaymentsCreate.as_view(), name="payments_create"),
    path("payments/update/<int:pk>/", PaymentsUpdate.as_view(), name="payments_update"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
] + router.urls

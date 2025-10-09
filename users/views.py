from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from lms.permissions import IsModerator

from .models import Payments, User
from .permissions import IsOwner
from .serializers import PaymentsSerializer, UserOwnerSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Класс реализует интерфейс для CRUD операция модели User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = (IsOwner,)
        elif self.action == "list":
            self.permission_classes = (IsModerator,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "retrieve" and self.request.user == self.get_object():
            return UserSerializer
        else:
            return UserOwnerSerializer


class PaymentsView(generics.ListAPIView):
    """Класс реализует интерфейс для вывода списка платежей"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["date_payment"]
    filterset_fields = ["method", "content_type"]

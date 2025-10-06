from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter

from .models import Payments, User
from .serializers import PaymentsSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Класс реализует интерфейс для CRUD операция модели User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentsView(generics.ListAPIView):
    """Класс реализует интерфейс для вывода списка платежей"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["date_payment"]
    filterset_fields = ["method", "content_type"]

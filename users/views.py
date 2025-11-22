from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from lms.models import Course, Lesson
from lms.permissions import IsModerator

from .models import Payments, User
from .permissions import IsOwner
from .serializers import PaymentsSerializer, UserOwnerSerializer, UserSerializer
from .services import create_checkout_session, create_price, create_product, retrieve_checkout_session


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


class PaymentsCreate(generics.CreateAPIView):
    """Класс реализует интерфейс для создания платежа"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        if str(payment.content_type) == "Lms | Курс":
            product = Course.objects.filter(pk=payment.object_id).values("name")
            product_name = "Курс " + product[0].get("name")
        else:
            product = Lesson.objects.filter(pk=payment.object_id).values("name")
            product_name = "Урок " + product[0].get("name")
        product_stripe = create_product(product_name)
        price = create_price(payment.amount, product_stripe)
        session_id, payment_link = create_checkout_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentsUpdate(generics.UpdateAPIView):
    """Класс реализует интерфейс для проверки статуса платежа"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    def perform_update(self, serializer):
        payment = serializer.save()
        status, payment_link = retrieve_checkout_session(payment.session_id)
        payment.status = status
        payment.save()

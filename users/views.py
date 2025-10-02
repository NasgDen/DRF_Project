
from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """ Класс реализует интерфейс для CRUD операция модели User """

    queryset = User.objects.all()
    serializer_class = UserSerializer

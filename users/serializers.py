from rest_framework import serializers

from .models import Payments, User


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payment = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone", "city", "avatar", "payment",)

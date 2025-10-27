from django.contrib import admin

from .models import Payments, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "phone",
        "avatar",
        "city",
    )
    list_filter = ("city",)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "date_payment",
        "content_type",
        "object_id",
        "paid_item",
        "method",
        "amount",
    )

from django.contrib import admin

from .models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image",
        "description",
        "owner",
    )
    list_filter = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image",
        "description",
        "link_to_video",
        "course",
        "owner",
    )
    list_filter = ("name",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "course",
    )
    list_filter = ("user",)

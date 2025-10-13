from django.template.context_processors import request
from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import LinkVideoValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validator = [LinkVideoValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
    subscription = serializers.SerializerMethodField()
    lessons_number = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson", many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "image",
            "description",
            "lessons",
            "lessons_number",
            "owner",
            "subscription",
        )

    def get_lessons_number(self, instance):
        """Функция подсчитывает количество уроков в курсе"""
        return Lesson.objects.filter(course=instance).count()

    def get_subscription(self, instance):
        """Функция реализует вывод о подписки на курс """
        user = self.context['request'].user
        return Subscription.objects.filter(course=instance, user=user).exists()

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
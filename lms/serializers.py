from rest_framework import serializers

from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lessons_number = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "name", "image", "description", "lessons_number")

    def get_lessons_number(self, instance):
        """Функция подсчитывает количество уроков в курсе"""
        return Lesson.objects.filter(course=instance).count()

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

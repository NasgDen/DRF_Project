from rest_framework import serializers

from .models import Course, Lesson
from .validators import LinkVideoValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validator = [LinkVideoValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
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
        )

    def get_lessons_number(self, instance):
        """Функция подсчитывает количество уроков в курсе"""
        return Lesson.objects.filter(course=instance).count()

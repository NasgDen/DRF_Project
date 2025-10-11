import re
from rest_framework.serializers import ValidationError


class LinkVideoValidator:
    """ Класс реализует валидацию поля link_to_video модели Lesson """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile('(?:https?://)?(?:www\.)?youtube\.com/watch\.?v=([a-zA-Z0-9_-]+)')
        tmp_value = dict(value).get(self.field)
        if not bool(reg.match(tmp_value)):
            raise ValidationError('Неверная ссылка на видео урока.')
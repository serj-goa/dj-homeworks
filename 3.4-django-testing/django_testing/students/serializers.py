from django.conf import settings
from rest_framework import serializers as s

from students.models import Course


class CourseSerializer(s.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, data):
        if len(data) > settings.MAX_STUDENTS_PER_COURSE:
            raise ValueError(f'Превышено количество студентов!\nМаксимум = {settings.MAX_STUDENTS_PER_COURSE}')

        return data

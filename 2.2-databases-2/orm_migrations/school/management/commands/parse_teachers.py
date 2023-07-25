import json

from django.core.management.base import BaseCommand

from school.models import Student


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('school.json', encoding='utf-8') as file:
            for data in json.load(file):
                if data['model'] == 'school.student':
                    student = Student.objects.get(id=data['pk'])
                    student.teachers.add(data['fields']['teacher'])

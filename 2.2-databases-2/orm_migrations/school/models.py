from django.db import models as m


class Teacher(m.Model):
    name = m.CharField(max_length=30, verbose_name='Имя')
    subject = m.CharField(max_length=10, verbose_name='Предмет')

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return self.name


class Student(m.Model):
    name = m.CharField(max_length=30, verbose_name='Имя')
    teachers = m.ManyToManyField(Teacher, related_name='students')
    group = m.CharField(max_length=10, verbose_name='Класс')

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return self.name

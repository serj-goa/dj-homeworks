from django.db import models as m
from django.forms import fields as f


class Sensor(m.Model):
    name = m.CharField(verbose_name='Название', max_length=60)
    description = m.CharField(verbose_name='Описание', max_length=1024)

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'

    def __str__(self):
        return f'{self.id} - {self.name}'


class Measurement(m.Model):
    sensor = m.ForeignKey(Sensor, on_delete=m.CASCADE, related_name='measurements')
    temperature = m.DecimalField(verbose_name='Температура', max_digits=3, decimal_places=1)
    created_at = m.DateTimeField(verbose_name='Дата измерения', auto_now_add=True)
    image = f.ImageField(max_length=128, allow_empty_file=True)

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'

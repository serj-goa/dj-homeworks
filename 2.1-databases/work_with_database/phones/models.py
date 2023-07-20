from django.db import models as m


class Phone(m.Model):

    name = m.CharField(verbose_name='Название', max_length=50)
    price = m.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = m.ImageField(verbose_name='Изображение')
    release_date = m.DateField(verbose_name='Дата выхода')
    lte_exists = m.BooleanField(verbose_name='Наличие LTE', default=True)
    slug = m.SlugField(max_length=255)

    def __str__(self):
        return self.name

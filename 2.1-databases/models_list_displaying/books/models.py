from django.db import models as m


class Book(m.Model):
    name = m.CharField(u'Название', max_length=64)
    author = m.CharField(u'Автор', max_length=64)
    pub_date = m.DateField(u'Дата публикации')

    def __str__(self):
        return f'{self.name} {self.author}'

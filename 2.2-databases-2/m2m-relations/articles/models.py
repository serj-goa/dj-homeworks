from django.db import models as m


class Article(m.Model):

    title = m.CharField(max_length=256, verbose_name='Название')
    text = m.TextField(verbose_name='Текст')
    published_at = m.DateTimeField(verbose_name='Дата публикации')
    image = m.ImageField(null=True, blank=True, verbose_name='Изображение')
    tags = m.ManyToManyField('Tag', through='Scope')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-published_at', )

    def __str__(self):
        return self.title


class Tag(m.Model):

    name = m.CharField(max_length=50, verbose_name='Название тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Scope(m.Model):

    article = m.ForeignKey(Article, on_delete=m.CASCADE, related_name='scopes')
    tag = m.ForeignKey(Tag, on_delete=m.CASCADE, related_name='scopes')
    is_main = m.BooleanField(default=False)

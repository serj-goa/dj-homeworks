from django.conf import settings
from django.db import models as m


class AdvertisementStatusChoices(m.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(m.Model):
    """Объявление."""

    title = m.TextField()
    description = m.TextField(default='')
    status = m.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete=m.CASCADE)
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Favorites(m.Model):
    """ Избранное. """

    user = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete=m.CASCADE)
    advertisement = m.ForeignKey(Advertisement, on_delete=m.CASCADE)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

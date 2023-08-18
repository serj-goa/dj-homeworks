from django.contrib.auth.models import User
from django.forms import ValidationError

from rest_framework import serializers as s

from advertisements.models import Advertisement, Favorites


class UserSerializer(s.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', )


class AdvertisementSerializer(s.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at', )
        read_only_fields = ['creator', ]

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        advs = Advertisement.objects.filter(
            creator=self.context['request'].user,
            status='OPEN'
        ).count()
        # status = data.get('status')

        if advs >= 10 and self.context['request'].method == 'POST':
            raise s.ValidationError('Максимальное число открытых объявлений: 10')

        return data


class FavoriteSerializer(s.ModelSerializer):
    advertisement = AdvertisementSerializer(read_only=True)

    class Meta:
        model = Favorites
        fields = ['id', 'advertisement', ]

    def validate(self, data):
        if Advertisement.objects.get(id=data['advertisement'].id).creator == data['user']:
            raise ValidationError('Своё объявление нельзя добавлять в избранное!')

        if Favorites.objects.filter(advertisement=data['advertisement'], user=data['user']):
            raise ValidationError('Это объявление уже есть в избранном')

        return data

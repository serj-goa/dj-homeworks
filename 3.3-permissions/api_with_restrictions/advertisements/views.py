from django.core.exceptions import ValidationError
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.viewsets import ModelViewSet

from .filters import AdvertisementFilter
from .models import Advertisement, Favorites
from .permissions import IsOwnerOrReadOnly
from .serializers import AdvertisementSerializer, FavoriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AdvertisementFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]

        return []

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Advertisement.objects.exclude(status='DRAFT')

        return Advertisement.objects.filter(Q(creator=self.request.user) | ~Q(status='DRAFT'))

    @action(detail=True, url_path='favorites', permission_classes=[IsAuthenticated(), ])
    def add_favorites_posts(self, request, pk):
        queryset = Advertisement.objects.get(id=pk)

        if queryset:
            validated_data = {
                'advertisement': queryset,
                'user': request.user,
            }
            serializer = FavoriteSerializer(data=validated_data)

            try:
                serializer.validate(data=validated_data)

            except ValidationError as err:
                print(err)
                return Response('Своё объявление нельзя добавлять в избранное!', status=HTTP_403_FORBIDDEN)

            serializer.create(validated_data)

            return Response('Пост добавлен в избранное')

    @action(
        detail=True,
        methods=['DELETE', ],
        url_path='delete',
        permission_classes=[IsAuthenticated(), IsOwnerOrReadOnly(), ]
    )
    def delete_favorites_posts(self, request, pk):
        Favorites.objects.get(advertisement__id=pk, user=request.user).delete()

        return Response('Пост удалён из избранного')

    @action(detail=False, methods=['GET', ], url_path='favorites_posts', permission_classes=[IsAuthenticated(), ])
    def show_favorites_posts(self, request):
        queryset = Favorites.objects.filter(user=request.user)
        serializer = FavoriteSerializer(queryset, many=True)

        return Response(serializer.data)

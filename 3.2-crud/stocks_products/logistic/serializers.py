from rest_framework import serializers as s

from .models import Product, Stock, StockProduct


class ProductSerializer(s.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', ]


class ProductPositionSerializer(s.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price', ]


class StockSerializer(s.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions', ]

    def create(self, validated_data):
        # получение связанных данных для других таблиц
        positions = validated_data.pop('positions')

        # создание склада по его параметрам
        stock = super().create(validated_data)

        # заполнение связанных таблиц через таблицу StockProduct с помощью списка positions
        for position in positions:
            StockProduct.objects.get_or_create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        # получение связанных данных для других таблиц
        positions = validated_data.pop('positions')

        # обновление склада по его параметрам
        stock = super().update(instance, validated_data)

        # обновление связанных таблиц через таблицу StockProduct с помощью списка positions
        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position.get('product'),
                defaults={
                    'price': position.get('price'),
                    'quantity': position.get('quantity')
                }
            )

        return stock

from django.core.validators import MinValueValidator
from django.db import models as m


class Product(m.Model):
    title = m.CharField(max_length=60, unique=True)
    description = m.TextField(null=True, blank=True)


class Stock(m.Model):
    address = m.CharField(max_length=200, unique=True)
    products = m.ManyToManyField(Product, through='StockProduct', related_name='stocks')


class StockProduct(m.Model):
    stock = m.ForeignKey(Stock, on_delete=m.CASCADE, related_name='positions')
    product = m.ForeignKey(Product, on_delete=m.CASCADE, related_name='positions')
    quantity = m.PositiveIntegerField(default=1)
    price = m.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(0)])

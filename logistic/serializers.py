from django.db import transaction
from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description')


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ('product', 'quantity', 'price')


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ('id', 'address', 'positions')

    def validate_positions(self, value):
        product_ids = [item['product'].pk for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError('Продукты на складе не должны повторяться.')
        return value

    @transaction.atomic
    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)
        StockProduct.objects.bulk_create([
            StockProduct(stock=stock, **position) for position in positions
        ])
        return stock

    @transaction.atomic
    def update(self, instance, validated_data):
        positions = validated_data.pop('positions', None)
        stock = super().update(instance, validated_data)
        if positions is not None:
            stock.positions.all().delete()
            StockProduct.objects.bulk_create([
                StockProduct(stock=stock, **position) for position in positions
            ])
        return stock

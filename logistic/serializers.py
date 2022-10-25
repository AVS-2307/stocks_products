from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']
    # настройте сериализатор для позиции продукта на складе


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, partial=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    # def update_or_create(self, instance, validated_data):
    #     # достаем связанные данные для других таблиц
    #     positions = validated_data.pop('positions')
    #     stock = super().update_or_create(instance, validated_data)
    #     StockProduct.objects.update_or_create(stock=['stock_id'], product=['product_id'], defaults={'price': positions.price, 'quantity': positions.quantity})
    #     return stock

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)
        # print(positions)
        return stock

    # настройте сериализатор для склада

    # def update(self, instance, validated_data):
    #     #     # достаем связанные данные для других таблиц
    #     positions = validated_data.pop('positions')
    #     #     # обновляем склад по его параметрам
    #     #     stock = super().update(instance, validated_data)
    #     stock = instance.positions
    #     # position_info
    #     instance.stock_id = validated_data.get('stock_id', instance.stock_id)
    #     instance.product_id = validated_data.get('product_id', instance.product_id)
    #     instance.quantity = validated_data.get('quantity', instance.quantity)
    #     instance.price = validated_data.get('price', instance.price)
    #     instance.save()
    #
    #     return stock

    def update(self, instance, validated_data):
        #     # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        #     # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        #     # в нашем случае: таблицу StockProduct
        #     # с помощью списка positions
        for position in positions:
            StockProduct.objects.update(**position)
        return stock

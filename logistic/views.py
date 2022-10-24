from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock, StockProduct
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['description', ]


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all().order_by('id')
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['id', 'address', 'products']
    filterset_fields = ['address', 'products']
    search_fields = ['products__description']  # поиск продукта на складах по названию

    # def get_serializer(self, instance=None, data=None, many=False, partial=False):
    #     """If request is not PUT, allow partial updates."""
    #     if self.request.method == 'PUT':
    #         return StockSerializer(instance=instance, data=data, many=many, partial=True)
    #     else:
    #         return StockSerializer(instance=instance, data=data, many=many, partial=partial)



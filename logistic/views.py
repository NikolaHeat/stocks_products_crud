from django.db.models import Q
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('title', 'description')
    pagination_class = StandardPagination


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all().order_by('id')
    serializer_class = StockSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('positions')
        product_id = self.request.query_params.get('products')
        search = self.request.query_params.get('search')
        if product_id:
            queryset = queryset.filter(products__id=product_id)
        if search:
            queryset = queryset.filter(
                Q(products__title__icontains=search)
                | Q(products__description__icontains=search)
            )
        return queryset.distinct()

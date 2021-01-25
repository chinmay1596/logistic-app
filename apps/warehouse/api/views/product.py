from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from apps.commons.utils.custom_pagination import CustomPagination
from apps.warehouse.api.serializers.product import ProductSerializer, WarehouseProductSerializer
from apps.warehouse.models import Product, WarehouseProduct, Shelf, Warehouse


class ProductCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    pagination_class = CustomPagination
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        shelf = Shelf.objects.get(id=2)
        warehouse_instance = Warehouse.objects.get(id=1)
        warehouse = WarehouseProduct.objects.create(
            warehouse=warehouse_instance, product=instance, units=instance.max_quantity, location=shelf)
        return Response({'data': serializer.data, 'success': True, 'message': 'Product created successfully'},
                        status=status.HTTP_201_CREATED)


class ProductRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class WarehouseProductAPIView(ListCreateAPIView):
    pagination_class = CustomPagination
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductSerializer

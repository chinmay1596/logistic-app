from django.urls import path

from apps.warehouse.api.views.product import ProductCreateAPIView, WarehouseProductAPIView, ProductRetrieveUpdateAPIView

app_name = 'product-api'

urlpatterns = [
    path('', ProductCreateAPIView.as_view(), name='api_create'),
    path('warehouse/assign', WarehouseProductAPIView.as_view(),
         name='warehouse_product_assign'),
    path('<int:pk>/', ProductRetrieveUpdateAPIView.as_view(), name='api_detail'),
]

from django.urls import path

from apps.warehouse.views.product import (
    ProductCreateView, ProductDeleteView, ProductListView, ProductQuantityUpdateView, LocationUpdateView
)
from apps.warehouse.views.warehouse import (
    WarehouseCreateView, WarehouseListView, WarehouseUpdateView,
    WarehouseDeleteView, ExportWarehouseView, ImportWarehouseView
)

app_name = 'warehouse'

urlpatterns = [
    path('', WarehouseListView.as_view(), name='list'),
    path('create/', WarehouseCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', WarehouseUpdateView.as_view(), name='detail'),
    path('delete/<int:pk>/', WarehouseDeleteView.as_view(), name='delete'),
    path('export/', ExportWarehouseView.as_view(), name='export'),
    path('import/', ImportWarehouseView.as_view(), name='import'),
    path('<int:warehouse_id>/product/create', ProductCreateView.as_view(), name='product-create'),
    path('<int:warehouse_id>/product/<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete'),
    path('<int:warehouse_id>/product/', ProductListView.as_view(), name='product-list'),
    path('quantity/', ProductQuantityUpdateView.as_view(), name='quantity-update'),
    path('location_update/', LocationUpdateView.as_view(), name='location-update')
]

from rest_framework.routers import DefaultRouter

from apps.warehouse.api.views.warehouse import WarehouseViewSet

app_name = 'warehouse-api'

router = DefaultRouter()

router.register(
    r'',
    WarehouseViewSet,
    basename='warehouse'
)

urlpatterns = router.urls

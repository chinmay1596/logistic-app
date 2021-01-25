from apps.commons.mixins.viewset_mixins import CustomizeModelViewSet
from apps.warehouse.api.serializers.warehouse import WarehouseSerializer
from apps.warehouse.models import Warehouse


class WarehouseViewSet(CustomizeModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = []

from rest_framework.serializers import ModelSerializer

from apps.warehouse.models import Warehouse


class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

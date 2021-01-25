from rest_framework import serializers
from apps.warehouse.models import Product, WarehouseProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'title', 'parent_product', 'description', 'product_type', 'is_discountable',
            'is_active', 'price_was', 'offer_price', 'units', 'packaging_instructions', 'image',
            'product_state'
        )


class WarehouseProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = WarehouseProduct
        fields = '__all__'

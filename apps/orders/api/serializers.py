from rest_framework import serializers

from apps.customer.models import Customer, Address
from apps.orders.constants import BUNDLE_CATEGORY
from apps.orders.models import Order, OrderItem, OrderBundle


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('address',)


class CreateOrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'uuid', 'warehouse', 'merchant', 'customer', 'address', 'latitude',
            'longitude', 'due_date', 'order_status', 'order_date', 'notes', 'payment_type', 'shipping_by', 'amount',
            'order_type', 'items'
        )
        extra_kwargs = {'warehouse': {'required': True},
                        'order_status': {'read_only': True}}

    @staticmethod
    def get_items(obj):
        return obj.items.all().values('id', 'product_id', 'units')


class OrderListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    customer = CustomerSerializer()
    address = serializers.CharField()

    class Meta:
        model = Order
        fields = (
            'id', 'uuid', 'warehouse', 'merchant', 'customer', 'address', 'latitude', 'longitude', 'due_date',
            'order_status', 'order_date', 'notes', 'payment_type', 'shipping_by', 'amount', 'order_type', 'items',
            'priority')

    @staticmethod
    def get_items(obj):
        return obj.items.all().values('id', 'product_id', 'units')


class OrderItemSerializer(serializers.Serializer):
    product = serializers.ListField(required=True)


class OrderDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    customer = CustomerSerializer()
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = (
            'id', 'uuid', 'warehouse', 'merchant', 'customer', 'address', 'latitude', 'longitude', 'due_date',
            'order_date', 'notes',
            'payment_type', 'shipping_by', 'amount', 'order_type', 'priority', 'reason_for_cancellation', 'items',
        )

    @staticmethod
    def get_items(obj):
        return obj.items.all().values('id', 'product_id', 'units')


class OrderUpdateSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    order_type = serializers.ChoiceField(choices=BUNDLE_CATEGORY)

    class Meta:
        model = Order
        fields = (
            'warehouse', 'merchant', 'customer', 'address', 'latitude', 'longitude', 'notes',
            'payment_type', 'shipping_by', 'amount', 'order_type', 'priority', 'items',
        )

    @staticmethod
    def get_items(obj):
        return obj.items.all().values('id', 'product_id', 'units')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class BundleSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = OrderBundle

        fields = (
            'bundle_id', 'total_volume', 'estimated_time', 'no_of_order', 'bundle_payment', 'storekeeper',
            'order')


class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'reason_for_cancellation')


class ReturnOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id',)

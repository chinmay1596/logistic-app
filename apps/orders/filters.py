import django_filters

from apps.orders.models import Order


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['order_status', 'warehouse']

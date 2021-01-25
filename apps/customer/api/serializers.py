from rest_framework import serializers
from apps.customer.models import Customer


class ListCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone')

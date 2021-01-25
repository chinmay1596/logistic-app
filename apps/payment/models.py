import uuid
from django.db import models
from apps.commons.models.commons import BaseModel
from apps.orders.constants import PAYMENT_CHOICES, CASH_ON_DELIVERY
from apps.orders.models import Order


class Transaction(BaseModel):
    transaction_id = models.CharField(unique=True, max_length=10)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='transaction_order')
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(
        choices=PAYMENT_CHOICES, max_length=64, default=CASH_ON_DELIVERY)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return f'Transaction Id: {self.transaction_id} -> Order Id: {self.order.id}'

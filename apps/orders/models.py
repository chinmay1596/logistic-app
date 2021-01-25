import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.shortcuts import reverse

from apps.commons.models.commons import BaseModel, UUIDModel
from apps.customer.models import Customer, Address
from apps.employee.models import Driver, StoreKeeper
from apps.orders.constants import (
    ORDER_STATUS, PAYMENT_CHOICES, CASH_ON_DELIVERY,
    BUNDLE_CATEGORY, PICK_UP, UNFULFILLED, BUNDLE_STATUS, PROCESSING, PRIORITY, MEDIUM)
from apps.warehouse.models import Warehouse, Product, WarehouseProduct
from utils.location_utils import calculate_distance_using_lat_lng

UserModel = get_user_model()


class Order(BaseModel):
    uuid = models.CharField(max_length=6, default='',
                            editable=True, unique=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL, related_name='warehouse', null=True, blank=True)
    merchant = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='order_merchant')
    order_status = models.CharField(
        max_length=20, choices=ORDER_STATUS, default=UNFULFILLED, null=True, blank=False)
    order_date = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name='customer_order', null=True,
                                 blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, help_text='Address of Order delivery.',
                                related_name='order_address')
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], help_text='Enter Values between -90 to 90',
        null=True, blank=True)
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], help_text='Enter Values between -180 to 180',
        null=True, blank=True)
    due_date = models.DateField(
        null=True, blank=True, help_text='Order due date.')
    notes = models.TextField(max_length=100000, null=True, blank=True,
                             help_text='Additional details regarding orders.')
    payment_type = models.CharField(
        max_length=25, choices=PAYMENT_CHOICES, default=CASH_ON_DELIVERY)
    shipping_by = models.CharField(
        max_length=20, null=True, blank=True, default='DHL')
    amount = models.FloatField(default=0.0)
    order_type = models.CharField(
        max_length=20, choices=BUNDLE_CATEGORY, default=PICK_UP)
    priority = models.PositiveIntegerField(
        choices=PRIORITY, default=MEDIUM, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    reason_for_cancellation = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.warehouse.name} -> Order Id: {self.id}'

    def get_distance(self):
        distance = calculate_distance_using_lat_lng(self.latitude, self.longitude, self.warehouse.latitude,
                                                    self.warehouse.longitude)
        if distance < self.warehouse.location_range:
            return True
        else:
            return False

    def get_date(self):
        date_diff = (datetime.date.today() - self.order_date).days
        return str(date_diff) + " days ago." if date_diff != 0 else "Today"

    def get_absolute_url(self):
        return reverse("orders:order_item", kwargs={
            'order_id': self.id
        })


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name='orders')
    units = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.product.title

    @property
    def amount(self):
        return int(self.product.offer_price) * self.units


class OrderBundle(BaseModel):
    order = models.ManyToManyField(Order, related_name='bundle')
    bundle_id = models.CharField(max_length=10, unique=True)
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='bundle_driver'
    )
    storekeeper = models.ForeignKey(
        StoreKeeper,
        related_name='bundle_storekeeper',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    total_volume = models.IntegerField(
        null=True, blank=True,
        help_text='Total weight of the order items.'
    )
    estimated_time = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(
        max_length=20,
        choices=BUNDLE_CATEGORY,
        default=PICK_UP
    )
    no_of_order = models.IntegerField(null=True, blank=True, default=1)
    bundle_payment = models.FloatField(
        null=True, blank=True, default=0,
        help_text="Total Payment of the bundle items"
    )
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=64,
        choices=BUNDLE_STATUS,
        default=PROCESSING
    )

    def __str__(self):
        return self.bundle_id

    def get_orders(self):
        queryset = OrderBundle.objects.get(
            id=self.id).order.values_list('latitude', 'longitude')
        return [list(ele) for ele in queryset]

    def get_warehouse_coordinates(self):
        queryset = OrderBundle.objects.get(id=self.id).order.values_list('warehouse__latitude',
                                                                         'warehouse__longitude').distinct()
        coordinates = [list(ele) for ele in queryset]
        final_coordinates = [coordinates[0][0], coordinates[0][1]]
        return final_coordinates

    def get_orderbundle_id_url(self):
        return reverse("orders:aggigndriver", kwargs={
            'bundle_id': self.bundle_id
        })


class OrderRemark(BaseModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='remark_order')
    detail = models.TextField(max_length=1000)

    def __str__(self):
        return f'{self.order.id} -> Remark: {self.detail}'

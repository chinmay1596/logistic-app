# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from apps.commons.models.commons import BaseModel, SerializedModal
from apps.employee.models import Driver
from apps.fleet.constants import VEHICLE_TYPES, VEHICLE_STATUS
from apps.warehouse.models import Warehouse
from apps.orders.models import OrderBundle

UserModel = get_user_model()


class Vehicle(BaseModel):
    merchant = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='merchant_vehicles')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, related_name='warehouses', null=True,
                                  blank=True)
    model_number = models.CharField(max_length=30)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    registration_number = models.CharField(max_length=30, unique=True)
    license_plate_number = models.CharField(max_length=30, unique=True)
    vehicle_status = models.CharField(max_length=20, choices=VEHICLE_STATUS, default='Active')

    def __str__(self):
        return self.license_plate_number

    def get_absolute_url(self):
        return reverse("fleet:vehicle_info", kwargs={
            'pk': self.id
        })

    @property
    def active_driver(self):
        history = self.driver_histories.filter(to_date__isnull=True).first()
        return history


class DriverHistory(BaseModel):
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, related_name='vehicle_histories', null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name='driver_histories', null=True)
    bundle = models.ForeignKey(OrderBundle, on_delete=models.SET_NULL, related_name='bundle_histories', null=True)
    from_date = models.DateTimeField(auto_now_add=True)
    to_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.driver.full_name} rides {self.vehicle.model_number}" \
               f"(Reg:{self.vehicle.registration_number}, License:{self.vehicle.license_plate_number})"


class SerializeDriverHistory(SerializedModal, DriverHistory):
    model_reference = {
        'id': 'id',
        'driver': {
            'id': 'driver.id',
            'full_name': 'driver.full_name',
            'bundle_driver': 'driver__bundle_driver'
        },
        'from_date': 'from_date',
        'to_date': 'to_date',

    }

    class Meta:
        proxy = True
        ordering = ['created_at']

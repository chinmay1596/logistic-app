from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from apps.commons.models.commons import BaseModel
from apps.employee.constants import (
    USER_TYPE_CHOICES, DRIVER_ORDER_STATUS, DRIVER_STATUS, TRANSPORTATION_TYPE,
    VEHICLE_TYPE, SHIFT_STATUS, STORE_KEEPER_SHIFT_STATUS, PENDING, MOTORBIKE,
    PRIVATE, ASSIGNED, ACTIVE, DRIVER
)

User = get_user_model()


class UserInvite(BaseModel):
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=DRIVER)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, related_name='user_invite', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.email, self.user_type)


class Driver(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    address = models.TextField(blank=True, max_length=1000)
    driving_license = models.CharField(max_length=60, blank=True, null=True)
    driver_status = models.CharField(max_length=30, choices=DRIVER_STATUS, default=ACTIVE)
    transportation = models.CharField(max_length=30, choices=TRANSPORTATION_TYPE, default=PRIVATE)
    shift_status = models.CharField(max_length=20, choices=SHIFT_STATUS, default=ASSIGNED)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE, default=MOTORBIKE)
    online_time = models.PositiveBigIntegerField(default=0, validators=[MinValueValidator(0)])
    Delivered = models.PositiveBigIntegerField(default=0, validators=[MinValueValidator(0)])
    break_time = models.PositiveBigIntegerField(default=0, validators=[MinValueValidator(0)])
    rating = models.DecimalField(max_digits=2, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    distance_travelled = models.DecimalField(max_digits=5, decimal_places=3, validators=[MinValueValidator(0)],
                                             default=0)
    orderStatus = models.CharField(max_length=30, choices=DRIVER_ORDER_STATUS, default=PENDING)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.user.full_name


class StoreKeeper(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='storekeeper')
    online_time = models.PositiveBigIntegerField(default=0, validators=[MinValueValidator(0)])
    complete_orders = models.PositiveBigIntegerField(default=0, validators=[MinValueValidator(0)])
    break_time = models.PositiveBigIntegerField(default=0, validators=[MinValueValidator(0)])
    shift_status = models.CharField(max_length=20, choices=STORE_KEEPER_SHIFT_STATUS, default=ASSIGNED)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.user.full_name

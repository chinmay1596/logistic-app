# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from apps.commons.models.commons import BaseModel
from apps.customer.constants import ADDRESS_CHOICES

UserModel = get_user_model()


class Customer(BaseModel):
    merchant = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True,
                                 related_name='customers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, unique=True, validators=[
        RegexValidator(regex=r'^(\+?\d{1,4})?(?!0+\s+,?$)\d{10}\s*,?$',
                       message="Enter a valid phone number")])

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Address(BaseModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='address')
    address_type = models.CharField(
        max_length=20, choices=ADDRESS_CHOICES, null=True)
    address = models.CharField(max_length=256, null=True, )
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], help_text='Enter Values between -90 to 90',
        null=True)
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], help_text='Enter Values between -180 to 180',
        null=True)

    class Meta:
        db_table = "address"

    def __str__(self):
        return self.address

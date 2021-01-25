import json

from django.conf import settings
from django.core.validators import MinValueValidator, FileExtensionValidator, MaxValueValidator
from django.db import models

from apps.commons.models.commons import BaseModel, SlugModel, UUIDModel, SerializedModal
from apps.commons.utils.commons import get_upload_path
from apps.warehouse.constants import LOCATION_RANGE_TYPE_OPTION, GEO_RADIUS, PRODUCT_STATE_OPTION, DRY


class Warehouse(BaseModel):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=1000, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    contact = models.CharField(max_length=16, blank=True)
    address = models.TextField(max_length=600, blank=True)
    longitude = models.FloatField(max_length=32, validators=[MinValueValidator(-180), MaxValueValidator(180)],
                                  null=True)
    latitude = models.FloatField(max_length=32, validators=[
        MinValueValidator(-90), MaxValueValidator(90)], null=True)
    location_range_type = models.CharField(
        max_length=12, choices=LOCATION_RANGE_TYPE_OPTION, default=GEO_RADIUS)
    location_range = models.PositiveBigIntegerField(
        default=5, validators=[MinValueValidator(0)])

    aisle_map = models.FileField(
        upload_to=get_upload_path,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.VALID_FILE_FORMATS.get('images'))
        ]
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Bay(BaseModel):
    name = models.CharField(max_length=32)
    abbreviation = models.CharField(max_length=8)

    def __str__(self):
        return f'{self.abbreviation}'


class Shelf(BaseModel):
    bay = models.ForeignKey(Bay, related_name='bay', on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    abbreviation = models.CharField(max_length=8)
    priority = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.location

    @property
    def location(self):
        return f'{str(self.bay)}-{self.abbreviation}'


class Product(BaseModel, SlugModel, UUIDModel):
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    parent_product = models.ForeignKey('self', related_name='child_products', on_delete=models.CASCADE, null=True,
                                       blank=True)
    description = models.TextField(max_length=10000, blank=True)
    product_type = models.CharField(max_length=32, blank=True)
    product_state = models.CharField(
        max_length=7,
        choices=PRODUCT_STATE_OPTION,
        default=DRY
    )
    is_discountable = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    price_was = models.FloatField(default=0, validators=[MinValueValidator(0)])
    offer_price = models.FloatField(
        default=0, validators=[MinValueValidator(0)])
    units = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(0)])
    packaging_instructions = models.TextField(max_length=10000, null=True)
    image = models.ImageField(upload_to='images/products/%Y-%m-%d/', null=True)
    location = models.ForeignKey(
        Shelf, related_name='shelf_products', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.title} -> {self.units}'


# TODO:remove this model with its dependencies
class WarehouseProduct(BaseModel, UUIDModel):
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    units = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(0)])
    location = models.ForeignKey(
        Shelf, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.warehouse} -> {self.product}'


class SerializeWarehouseProduct(SerializedModal, WarehouseProduct):
    model_reference = {
        'product': {
            'id': 'product.id',
            'title': 'product.title',
            'slug': 'product.slug',
            'product_code': 'product.uuid',
            'product_type': 'product.product_type',
            'is_discountable': 'product.is_discountable',
            'is_active': 'product.is_active',
            'price_was': 'product.price_was',
            'offer_price': 'product.offer_price',
            'units': 'product.units',
            'max_quantity': 'product.max_quantity',
            'min_quantity': 'product.min_quantity'
        },
        'units': 'units',
        'location': 'location'
    }

    class Meta:
        proxy = True
        ordering = ['id']

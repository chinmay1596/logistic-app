from django.contrib import admin
# Register your models here.
from django.contrib.admin import ModelAdmin

from apps.warehouse.models import (
    Warehouse, Product, Bay, Shelf, WarehouseProduct)


class WareHouseAdmin(ModelAdmin):
    list_display = ['name', 'email', 'contact', 'longitude', 'latitude',
                    'location_range_type', 'location_range']


admin.site.register(Warehouse, WareHouseAdmin)
admin.site.register(Product)


class ShelfAdmin(ModelAdmin):
    list_display = ['name', 'abbreviation', 'location', 'priority']


admin.site.register(Shelf, ShelfAdmin)
admin.site.register(Bay)


class WarehouseProductAdmin(ModelAdmin):
    list_display = ['warehouse', 'product', 'units', 'location']


admin.site.register(WarehouseProduct, WarehouseProductAdmin)

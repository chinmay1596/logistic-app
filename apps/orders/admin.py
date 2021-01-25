from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import Order, OrderItem, OrderBundle, OrderRemark

admin.site.register(Order)
admin.site.register(OrderBundle)
admin.site.register(OrderItem)
admin.site.register(OrderRemark)

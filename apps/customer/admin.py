from django.contrib import admin

# Register your models here.
from .models import Customer, Address
from django.contrib.admin import ModelAdmin


class CustomerAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name', 'merchant', 'email', 'phone']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address)

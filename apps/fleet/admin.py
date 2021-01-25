from django.contrib import admin

# Register your models here.
from apps.fleet.models import Vehicle
admin.site.register(Vehicle)

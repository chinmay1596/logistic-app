from django.contrib import admin
from .models import User, Address

# Register your models here.
admin.site.register(Address)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    fields = (
        'email', 'phone', 'password', 'first_name', 'last_name', 'address',
        'is_verified', 'image', 'is_staff', 'is_superuser', 'is_active',
        'last_login', 'user_type')
    list_filter = ('user_type',)

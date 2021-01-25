# Register your models here.
from django.contrib import admin
from apps.notification.models import Notification
from django.contrib.admin import ModelAdmin


class NotificationAdmin(ModelAdmin):
    list_display = ['user', 'title', 'message', 'data', 'read']


admin.site.register(Notification, NotificationAdmin)

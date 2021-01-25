from django.contrib import admin
from .models import Ticket, Chat, Documents
# Register your models here.

admin.site.register(Ticket)
admin.site.register(Chat)
admin.site.register(Documents)

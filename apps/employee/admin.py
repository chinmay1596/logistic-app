from django.contrib import admin



from apps.employee.models import UserInvite, Driver, StoreKeeper
admin.site.register(UserInvite)
admin.site.register(Driver)
admin.site.register(StoreKeeper)
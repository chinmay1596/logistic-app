from django.urls import path
from apps.customer.views import (
    CustomerExport, AddCustomerView, CustomerListView
)

app_name = 'customer'
urlpatterns = [
    path('', CustomerListView.as_view(), name='list'),
    path('add_customer/', AddCustomerView.as_view(), name='create'),
    path('export/', CustomerExport.as_view(), name="customer_export"),

]

from django.urls import path
from .views import (CustomerAPIView)

app_name = 'customer_api'
urlpatterns = [
    path('add_customer/', CustomerAPIView.as_view(), name='add_customer'),
]

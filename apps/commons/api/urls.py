from django.urls import path, include

app_name = 'api_v1'
urlpatterns = [
    path('customer/', include('apps.customer.api.urls', namespace='customer_api')),
    path('employee/', include('apps.employee.api.urls', namespace='employee_api')),
    path('support/', include('apps.support.api.urls', namespace='support-api')),
    path('account/', include('apps.account.api.urls', namespace='user_api')),
    path('product/', include('apps.warehouse.api.urls.product', namespace='product-api')),
    path('warehouse/', include('apps.warehouse.api.urls.warehouse', namespace='warehouse-api')),
    path('orders/', include('apps.orders.api.urls', namespace='order_api')),
]

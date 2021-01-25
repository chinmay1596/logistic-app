from .views import (OrderCreateAPIView, OrderRetrieveUpdateAPIView, BundleRetrieveAPIView, CancelOrderAPIView,
                    ReturnOrderAPIView)
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = 'orders'

router.register('order_bundle', BundleRetrieveAPIView, basename='order_bundle'),
router.register('order_cancel', CancelOrderAPIView, basename='order_cancel'),
router.register('order_return', ReturnOrderAPIView, basename='order_return'),

urlpatterns = router.urls

urlpatterns += [
    path('', OrderCreateAPIView.as_view(), name='create_order'),
    path('<int:pk>/', OrderRetrieveUpdateAPIView.as_view(), name='order_detail'),
]

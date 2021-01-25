from django.urls import path
from apps.orders.views import (OrderListView, DeliveryPartnerView, AssignOrderBundleView, OrderItemView,
                               OrderProcessView, AssignDriver, OrderBundleListView, OrderBundleDetailView,
                               OrderDetailView, CancelOrderView, ExportOrderItemView, capture_payment,
                               AddToExistingBundleView, PriorityOrderView)

app_name = 'orders'
urlpatterns = [

    # path('<int:pk>/', OrderListView.as_view(), name='order'),
    path('', OrderListView.as_view(), name='order'),
    # path('bundles/<int:pk>/', OrderBundleListView.as_view(), name='bundles'),
    path('bundles/', OrderBundleListView.as_view(), name='bundles'),
    path('bundles/detail/<int:pk>/', OrderBundleDetailView.as_view(), name='bundle-detail'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('capture/<int:pk>/', capture_payment, name='order-capture'),
    path('order_item/<order_id>/', OrderItemView.as_view(), name='order_item'),
    path('export/<int:pk>/', ExportOrderItemView.as_view(), name='export_order_item'),
    path('add-to-bundle/<int:pk>/', AddToExistingBundleView.as_view(), name='add_to_bundle'),
    path('delivery_partner/', DeliveryPartnerView.as_view(), name='delivery_partner'),
    path('assign_order_bundle/', AssignOrderBundleView.as_view(), name='assign_order_bundle'),
    path('process_order/', OrderProcessView.as_view(), name="process_order"),
    path('cancel/', CancelOrderView.as_view(), name="cancel_order"),
    path('aggigndriver/', AssignDriver.as_view(), name="aggigndriver"),
    path('priority/', PriorityOrderView.as_view(), name="assign_priority"),
]

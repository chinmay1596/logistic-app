from django.urls import path
from apps.notification.views import (CreateTokenView, NotificationListView, MarkReadNotificationView)

app_name = 'notification'

urlpatterns = [
    path('create_token/', CreateTokenView.as_view(), name='create_token'),
    path('show_notification/<int:pk>/', NotificationListView.as_view(), name='show_notification'),
    path('mark_notification/<int:pk>/', MarkReadNotificationView.as_view(), name='mark_notification')
]

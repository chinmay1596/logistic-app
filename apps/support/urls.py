from django.urls import path

from apps.support.views import SupportListView, SupportChatView
from . import views

app_name = 'support'

urlpatterns = [
    path('', SupportListView.as_view(), name='support'),
    path('ticket/<int:pk>/reply/', SupportChatView.as_view(), name='support-reply'),
]

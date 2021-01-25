from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TicketCreateViewset, TicketDetailViewset

app_name = 'support-api'

router = DefaultRouter()

router.register('', TicketCreateViewset, basename='support')
router.register('detail', TicketDetailViewset, basename='detail')

urlpatterns = router.urls

from django.urls import path
from rest_framework.routers import DefaultRouter
from ..views import AssignEmployeeShift, AssignEmployeeBundle

app_name = 'employee_api'

router = DefaultRouter()

router.register(
    r'(?P<employee_type>(driver|storekeeper))/(?P<employee_id>[\d]+)/shift/(?P<shift_status>(end|start|off-duty))',
    AssignEmployeeShift,
    basename='assign-shift'
)

urlpatterns = router.urls

from django.urls import path, re_path
from django.views.generic import TemplateView

from apps.employee import views
from apps.employee.views import (
    EmployeeInvitationView, EmployeeListView, EmployeeRegistrationView, EmployeeActivityView, AssignEmployeeBundle
)

app_name = 'employee'

urlpatterns = [
    re_path(
        r'(?P<employee_type>(driver|storekeeper))/invite/',
        EmployeeInvitationView.as_view(),
        name='send_invitation'
    ),
    re_path(
        r'(?P<employee_type>(driver|storekeeper))/assign/bundle',
        AssignEmployeeBundle.as_view(),
        name="assign_bundle"
    ),
    re_path(
        r'(?P<employee_type>(driver|storekeeper))/(?P<pk>\d+)/(?P<activity_type>(orders|shifts))',
        EmployeeActivityView.as_view(),
        name='employee-activity'
    ),
    re_path(
        r'(?P<employee_type>(driver|storekeeper))/(?P<display_type>(shift))/',
        EmployeeListView.as_view(),
        name='employee-shift'
    ),
    re_path(
        r'(?P<employee_type>(driver|storekeeper))/',
        EmployeeListView.as_view(),
        name='list-employee'
    ),
    path('register/<uidb64>/', EmployeeRegistrationView.as_view(), name='register'),
    path('activated/', TemplateView.as_view(template_name='employee/activated.html'), name='activated'),
    path('assign-store-keeper/<int:storekeeper_id>/<bundle_id>/', views.assignstorekeeper, name='assign_store_keeper'),
]

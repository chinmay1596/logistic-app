from django.urls import path
from apps.fleet.views import VehicleView, AddVehicleView, VehicleInfo, ChangeDriverView, DriverHistoryListView
from django.urls import path

from apps.fleet.views import VehicleView, AddVehicleView, VehicleInfo, VehicleDiscontinued

app_name = 'fleet'

urlpatterns = [
    path('', VehicleView.as_view(), name='vehicle'),
    path('add_vehicle', AddVehicleView.as_view(), name='add_vehicle'),
    path('vehicle_info/<int:pk>', VehicleInfo.as_view(), name='vehicle_info'),
    path('<int:pk>/change/driver/', ChangeDriverView.as_view(), name='change_driver'),
    path('<int:vehicle_id>/driver/histories/', DriverHistoryListView.as_view(), name='driver-history'),
    path('discontinued/', VehicleDiscontinued.as_view(), name='discontinued'),
    path('history/<int:pk>/', VehicleDiscontinued.as_view(), name='history')
]

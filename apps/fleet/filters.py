import django_filters

from apps.fleet.models import Vehicle


class VehicleFilter(django_filters.FilterSet):
    class Meta:
        model = Vehicle
        fields = ['vehicle_status']
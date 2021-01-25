from apps.commons.mixins.commons import DynamicFieldsModelForm
from apps.fleet.models import Vehicle


class AddVehicleForm(DynamicFieldsModelForm):
    class Meta:
        model = Vehicle
        fields = ['model_number', 'registration_number', 'license_plate_number', 'vehicle_type']
        placeholder = {
            'model_number': 'Model Number',
            'registration_number': 'Registration Number',
            'license_plate_number': 'License Plate Number'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vehicle_type = self.fields['vehicle_type'].widget.choices
        self.fields['vehicle_type'].widget.choices = tuple([(u'', 'Vehicle Type')] + list(vehicle_type[1:]))

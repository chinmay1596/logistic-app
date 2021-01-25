from django.urls import reverse_lazy

from apps.commons.mixins.commons import CustomCreateView, CustomListView, CustomUpdateView, CustomExportView, \
    CustomImportView
from apps.commons.mixins.commons import CustomDeleteView
from apps.warehouse.constants import GEO_RADIUS, MAPPING, TIME_RADIUS
from apps.warehouse.forms import WareHouseForm, ProductForm
from apps.warehouse.models import Warehouse


class WarehouseCreateView(CustomCreateView):
    model = Warehouse
    form_class = WareHouseForm
    success_url = reverse_lazy('warehouse:list')
    template_name = 'warehouse/create.html'


class WarehouseListView(CustomListView):
    queryset = Warehouse.objects.all()
    template_name = 'warehouse/list.html'

 
class WarehouseUpdateView(CustomUpdateView):
    queryset = Warehouse.objects.all()
    form_class = WareHouseForm
    template_name = 'warehouse/detail.html'
    extra_context = {
        'product_form': ProductForm()
    }
    success_url = reverse_lazy('warehouse:list')


class WarehouseDeleteView(CustomDeleteView):
    model = Warehouse
    success_url = reverse_lazy('warehouse:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = reverse_lazy('warehouse:detail', kwargs={'pk': self.object.id})
        return context


class ExportWarehouseView(CustomExportView):
    model = Warehouse
    related_names = {
        'NAME': 'name',
        'DESCRIPTION': 'description'
    }


class ImportWarehouseView(CustomImportView):
    failed_url = reverse_lazy('warehouse:create')
    success_url = reverse_lazy('warehouse:list')
    import_form_class = WareHouseForm
    import_fields = [
        'NAME',
        'DESCRIPTION',
        'EMAIL',
        'CONTACT',
        'ADDRESS',
        'LONGITUDE',
        'LATITUDE',
        'LOCATION RANGE TYPE',
        'LOCATION RANGE',
    ]
    values = [
        'Warehouse 1',
        'This description section.',
        'example@abc.com',
        '1234567890',
        'Xyz galli, Samsan Nagar',
        22.05,
        77.55,
        GEO_RADIUS,
        5
    ]
    model_fields_map = {
        'NAME': 'name',
        'DESCRIPTION': 'description',
        'EMAIL': 'email',
        'CONTACT': 'contact',
        'ADDRESS': 'address',
        'LONGITUDE': 'longitude',
        'LATITUDE': 'latitude',
        'LOCATION RANGE TYPE': 'location_range_type',
        'LOCATION RANGE': 'location_range',
    }
    queryset_fields_map = {
        'location_range_type': [GEO_RADIUS, MAPPING, TIME_RADIUS]
    }
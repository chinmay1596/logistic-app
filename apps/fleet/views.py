# Create your views here.
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from apps.notification.models import Notification
from apps.commons.mixins.commons import CustomListView, CustomCreateView, CustomDetailView, CustomAjaxUpdateView, \
    CustomAjaxListView, ListWithFilterAndSearchMixin
from apps.employee.forms import DriverListForm
from apps.fleet.constants import ACTIVE, INACTIVE, DISCONTINUED
from apps.fleet.filters import VehicleFilter
from apps.fleet.forms import AddVehicleForm
from apps.fleet.models import Vehicle, DriverHistory, SerializeDriverHistory
from apps.orders.models import OrderBundle, Order
from django.views.generic.base import View
from ..commons.utils.commons import SearchFilter
import random

UserModel = get_user_model()


class VehicleView(ListWithFilterAndSearchMixin):
    queryset = Vehicle.objects.all().order_by('-id')
    template_name = 'fleet/fleet.html'
    paginate_by = 10
    filter_backends = [SearchFilter]
    search_fields = ['id', 'model_number', 'vehicle_type', 'registration_number', 'license_plate_number',
                     'vehicle_status']

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        vehicle_filters = VehicleFilter(self.request.GET, queryset=queryset)
        return vehicle_filters.qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({

            'active': ACTIVE,
            'inactive': INACTIVE,
            'discontinued': DISCONTINUED,
            'form': AddVehicleForm(),
            'status': self.request.GET.get('vehicle_status'),

        })
        return context


class AddVehicleView(CustomCreateView):
    model = Vehicle
    form_class = AddVehicleForm
    template_name = 'fleet/fleet.html'
    success_url = reverse_lazy('fleet:vehicle')
    paginated_by = 10

    def form_valid(self, form):
        form.instance.merchant = self.request.user
        self.object = form.save()
        messages.success(self.request, 'Vehicle add successfully !')
        return HttpResponseRedirect(self.get_success_url())


class VehicleInfo(ListWithFilterAndSearchMixin):
    queryset = DriverHistory.objects.all().order_by('-id')
    template_name = 'fleet/vehicle_information.html'
    paginate_by = 7
    filter_backends = [SearchFilter]
    search_fields = ['id', 'driver__user__first_name', 'driver__user__last_name', 'bundle__bundle_id',
                     'bundle__total_volume', 'bundle__created_at']

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        vehicle_id = self.kwargs['pk']
        queryset = queryset.filter(vehicle_id=vehicle_id)
        return queryset

    def get_context_data(self, *args, **kwargs):
        vehicle_id = self.kwargs['pk']
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'form': DriverListForm(),
            'vehicle_info': Vehicle.objects.get(id=vehicle_id)
        })
        return ctx


class ChangeDriverView(CustomAjaxUpdateView):

    model = Vehicle
    driver_object = None

    def get_form(self, form_class=None):
        return DriverListForm(data=self.request.POST)

    def form_valid(self, form):
        self.perform_create(form)
        serialized_object = serialize('json', [self.driver_object])
        return JsonResponse({'instance': serialized_object}, status=200)

    def perform_create(self, form):
        instance = self.get_object()
        current_driver = instance.active_driver
        if current_driver:
            current_driver.to_date = timezone.now().astimezone()
            current_driver.save()

        new_driver = form.cleaned_data.get('drivers')
        bundle = OrderBundle.objects.filter(driver=new_driver).last()
        self.driver_object = DriverHistory.objects.create(vehicle=instance, driver=new_driver, bundle=bundle)


class DriverHistoryListView(CustomAjaxListView):
    paginate_by = 5
    allow_empty_first_page = False

    def get_queryset(self):
        return SerializeDriverHistory.objects.filter(
            vehicle=self.kwargs.get('vehicle_id'),
            to_date__isnull=False
        ).select_related('driver')


class VehicleDiscontinued(View):
    def post(self, request, *args, **kwargs):
        if self.request.POST.get('attendence'):
            data = self.request.POST.get('attendence').split(',')
            Vehicle.objects.filter(id__in=[vehicle_id for vehicle_id in data]).update(vehicle_status=DISCONTINUED)
            messages.success(request, 'Vehicle Discontinued successfully.')
        return redirect('fleet:vehicle')

import googlemaps
from django.contrib import messages
from django.db.models import Sum, Count
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.list import MultipleObjectMixin

from Helo_logistics.settings import GOOGLE_MAPS_API_KEY
from apps.orders.models import *
from apps.employee.models import *
from django.views.generic import ListView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.location_utils import (fetch_all_the_orders_of_warehouse_within_georadius, sort_and_fetch_orders,
                                  bundle_orders)
from utils.tokens import create_new_ref_number
from .constants import ACTIVE, RETURN, CANCELLED, DELIVERED, UNFULFILLED, DELIVERY, MEDIUM, HIGH, LOW
from django.utils.datastructures import MultiValueDictKeyError
from .filters import OrderFilter
from .forms import OrderProcessForm, OrderBundleForm, OrderRemarkForm
from ..account.constants import DRIVER
from ..commons.mixins.commons import (CustomListView, CustomCreateView, CustomDetailView, CustomUpdateView,
                                      ListWithFilterAndSearchMixin, CustomExportView)
from apps.employee.models import *
from ..commons.utils.commons import SearchFilter
from ..payment.models import Transaction
from django.views.generic.base import TemplateView

UserModel = get_user_model()


class OrderListView(ListWithFilterAndSearchMixin):
    template_name = 'orders/order.html'
    paginate_by = 10
    filter_backends = [SearchFilter]
    search_fields = ['id', 'address__address', 'customer__first_name', 'customer__last_name',
                     'priority']
    queryset = Order.objects.all().order_by('priority')

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        geo_radius = self.request.GET.get('geo_radius')

        if geo_radius:
            orders = fetch_all_the_orders_of_warehouse_within_georadius(self.request, queryset, int(geo_radius))
            final_queryset = Order.objects.filter(id__in=[order_id['order_id'] for order_id in orders])
            order_filters = OrderFilter(self.request.GET, queryset=final_queryset)
        else:
            order_filters = OrderFilter(self.request.GET, queryset=queryset)
        return order_filters.qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'user': UserModel.objects.all(),
            'active': ACTIVE,
            'unfulfilled': UNFULFILLED,
            'delivered': DELIVERED,
            'return': RETURN,
            'cancel': CANCELLED,
            'low': LOW,
            'medium': MEDIUM,
            'high': HIGH,
            'geo_radius': self.request.GET.get('geo_radius') if self.request.GET.get('geo_radius') else '',
            'qs': self.request.GET.get("search"),
            'order_status': self.request.GET.get('order_status')
        }
        )
        return context


class OrderProcessView(CustomCreateView):
    template_name = 'orders/process_order.html'
    form_class = OrderProcessForm

    def post(self, request, *args, **kwargs):
        data = self.request.POST.get('attendence').split(',')
        orders = Order.objects.filter(id__in=[order_id for order_id in data])
        sorted_orders = sort_and_fetch_orders(self.request, orders)
        bundle_lists = bundle_orders(sorted_orders, 5)
        for keys, values in bundle_lists.items():
            order_ids = [order_id['order_id'] for order_id in values]
            count = str(OrderBundle.objects.all().count())
            orders_list = Order.objects.filter(id__in=order_ids)
            total_payment = orders_list.aggregate(Sum('amount'))
            no_of_orders = orders_list.count()
            order_bundle_obj = OrderBundle.objects.create(bundle_id="BUN" + count, no_of_order=no_of_orders,
                                                          bundle_payment=total_payment['amount__sum'])
            order_bundle_obj.order.set(order_ids)
            orders_list.update(order_status=ACTIVE)
            Order.objects.filter(id__in=order_ids)
        return redirect('orders:bundles')


class OrderBundleListView(CustomListView):
    queryset = OrderBundle.objects.all().distinct()
    template_name = 'orders/process_order.html'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        bundles = OrderBundle.objects.all().distinct()
        warehouse = Warehouse.objects.get(id=1)
        context.update(
            {
                'order_bundle': bundles,
                'order_count': bundles.aggregate(Sum('no_of_order'))['no_of_order__sum'],
                # 'pk': self.kwargs['pk'],
                'warehouse_location': [warehouse.longitude, warehouse.latitude],
            }
        )
        return context


class OrderBundleDetailView(CustomDetailView):
    queryset = OrderBundle.objects.all()
    # form_class = OrderBundleForm
    template_name = 'orders/orderbundle_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        bundles = OrderBundle.objects.all().distinct()
        bundle_object = self.get_object()
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        warehouse_address = self.get_object().get_warehouse_coordinates()
        waypoints = self.get_object().get_orders()
        directions_result = gmaps.directions(warehouse_address, waypoints[-1],
                                             mode="driving", optimize_waypoints=True,
                                             avoid="ferries",
                                             )

        context.update(
            {
                'order_bundle': bundles,
                # 'order_count': bundles.aggregate(Sum('no_of_order'))['no_of_order__sum'],
                'order_count': bundle_object.order.all().count(),
                # 'pk': self.kwargs['pk'],
                # 'warehouse_location': [warehouse.longitude, warehouse.latitude],
                'drivers': UserModel.objects.filter(user_type=DRIVER),
                'orders': bundle_object.order.all(),
                'warehouse_location': self.get_object().get_warehouse_coordinates,
                'pk': bundle_object.id,
                'pickup_count': bundle_object.order.filter(order_type=PICK_UP).count(),
                'deliveries_count': bundle_object.order.filter(order_type=DELIVERY).count(),
                # 'ETA': directions_result[0]['legs'][0]['duration']['text'],
                'status': ['Processing', 'Pick Up List Generation', 'Store Keeper Assigned', 'Driver Assigned',
                           'Driver Out', 'Delivered'],
            }
        )
        return context

    def get_success_url(self):
        return reverse_lazy('orders:bundle-detail', kwargs={'pk': self.get_object().id})


class OrderDetailView(CustomDetailView, MultipleObjectMixin):
    queryset = Order.objects.all()
    template_name = 'orders/order_detail.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = self.object.items.filter()
        try:
            order_bundle = self.get_object().bundle.get()
        except OrderBundle.DoesNotExist:
            order_bundle = None
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(
            {
                'order_bundle': order_bundle,
                'form': OrderRemarkForm(),
                'remarks': OrderRemark.objects.filter(order=self.get_object()),
                # 'is_paid': Transaction.objects.get(order=self.get_object()).is_paid,
                'bundles': OrderBundle.objects.filter(order__warehouse=self.get_object().warehouse).distinct()
            }
        )
        return context

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        form = OrderRemarkForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.order = order
            obj.save()
        return redirect('orders:order-detail', order.pk)


class CancelOrderView(View):
    def post(self, request, *args, **kwargs):
        if self.request.POST.get('attendence'):
            data = self.request.POST.get('attendence').split(',')
            Order.objects.filter(id__in=[order_id for order_id in data]).update(order_status=CANCELLED)
            messages.success(request, 'Order cancelled successfully.')
        return redirect('orders:order')


class OrderItemView(ListView):
    queryset = OrderItem.objects.all()
    template_name = 'orders/OrderBundle.html'
    paginate_by = 10

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        queryset = super().get_queryset()
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        return queryset

    def get_context_data(self, *args, **kwargs):
        order_id = self.kwargs['order_id']
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'order': Order.objects.filter(id=order_id).distinct('id')
        }
        )
        return context


class ExportOrderItemView(CustomExportView):
    model = OrderItem
    related_names = {
        'Product Code': 'product.location.location',
        'Item Name': 'product.product.title',
        'Quantity': 'units',
        'Item Description': 'product.product.description',
        'Location In Aisle Map': 'product.location.location',
        'Packaging Instructions': 'product.product.packaging_instructions',
    }

    def get_queryset(self):
        order = Order.objects.get(id=self.kwargs['pk'])
        items = order.items.all()
        return items


def capture_payment(request, pk):
    order_obj = get_object_or_404(Order, pk=pk)
    transaction_id = create_new_ref_number()
    transaction, created = Transaction.objects.get_or_create(order=order_obj,
                                                             defaults={'transaction_id': transaction_id,
                                                                       'amount': order_obj.amount, 'is_paid': True})
    if created:
        order_obj.is_paid = True
        order_obj.save()
    return redirect('orders:order-detail', pk)


class AddToExistingBundleView(View):
    def post(self, request, *args, **kwargs):
        if self.request.POST.get('attendence'):
            data = self.request.POST.get('attendence').split(',')
            order_obj = Order.objects.get(id=self.kwargs['pk'])
            bundle_obj = OrderBundle.objects.get(id=data[0])
            bundle_obj.order.add(order_obj)
            bundle_obj.no_of_order = bundle_obj.order.all().count()
            bundle_obj.save()
            order_obj.order_status = ACTIVE
            order_obj.save()
            messages.success(request, 'Order added to selected bundle successfully.')
        return redirect('orders:order-detail', pk=self.kwargs['pk'])


class AssignDriver(CustomListView):
    queryset = User.objects.filter(user_type='Driver')
    template_name = 'employee/drivers-shifts.html'
    context_object_name = 'drivers'
    paginate_by = 3


class DeliveryPartnerView(TemplateView):
    template_name = 'orders/delivery-partner.html'


class AssignOrderBundleView(TemplateView):
    template_name = 'orders/assign-orderbundle.html'


class PriorityOrderView(View):
    def post(self, request, *args, **kwargs):
        if self.request.POST.get('attendence'):
            data = self.request.POST.get('attendence').split(',')
            priority = self.request.POST.get('priority')
            Order.objects.filter(id__in=[order_id for order_id in data]).update(priority=priority)
            messages.success(request, 'Priority set successfully.')
        return redirect('orders:order')

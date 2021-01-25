import ast
from django.db.models import Count, Q
from apps.employee.models import Driver
from apps.orders.models import Order, OrderBundle
from .forms import AnalyticsFilterForm
from ..commons.mixins.commons import CustomListView, CustomExportView
from apps.orders.constants import DELIVERED, CANCELLED, UNFULFILLED, ACTIVE
import datetime

now = datetime.datetime.now()


class BaseDataForAnalytics:
    query_dict = {
        'late_orders': Order.objects.filter((Q(order_status=ACTIVE) | Q(order_status=UNFULFILLED)),
                                            due_date__lte=now.date()).order_by('-due_date'),
        'cancelled_orders': Order.objects.filter(order_status=CANCELLED),
        'delivered_orders': Order.objects.filter(order_status=DELIVERED),
        'times_per_waypoints': OrderBundle.objects.all(),
        'active_drivers': Driver.objects.all(),
        'order_per_location': Order.objects.order_by('address').annotate(the_count=Count('address')),
        'reconciliation': Driver.objects.all(),
    }
    filter_dict = {

        'late_orders': ('bundle__driver_id__in', 'order_date__range'),
        'cancelled_orders': ('bundle__driver_id__in', 'order_date__range'),
        'delivered_orders': ('bundle__driver_id__in', 'order_date__range'),
        'times_per_waypoints': ('driver_id__in', 'created_at__range'),
        'active_drivers': ('id__in', 'bundle_driver__created_at__range'),
        'order_per_location': ('bundle__driver_id__in', 'order_date__range'),
        'reconciliation': ('id__in', 'bundle_driver__created_at__range'),
    }
    related_names = {
        'late_orders': {
            'ID': 'id',
            'Customer': 'customer.first_name',
            'Phone': 'customer.phone',
            'Address': 'address.address'
        },
        'cancelled_orders': {
            'ID': 'id',
            'Customer': 'customer.first_name',
            'Address': 'address.address',
            'Phone': 'customer.phone',
            'Created Time': 'order_date',
            'Scheduled Time': 'due_date',
        },
        'delivered_orders': {
            'ID': 'id',
            'Customer': 'customer.first_name',
            'Address': 'address.address',
            'Phone': 'customer.phone',
            'Created Time': 'order_date',
            'Scheduled Time': 'due_date',
        },
        'active_drivers': {
            'ID': 'id',
            'Name': 'user.get_full_name'
        },
        'times_per_waypoints': {
            'ID': 'id',
            'BUNDLE CREATED TIME': 'created_at',
            'Driver ID': 'driver.id',
            'DRIVER NAME': 'driver.user.get_full_name',
            'STATUS': 'status',
            'TIME TAKEN': 'estimated_time',
        },
        'order_per_location': {
            'ID': 'id',
            'LOCATION': 'address.address',
        }

    }

    def get_context_data(self, *args, object_list=None, **kwargs):

        # for dynamic select driver on template
        select_driver = self.request.GET.getlist('driver')
        for driver in range(0, len(select_driver)):
            select_driver[driver] = int(select_driver[driver])

        context = super().get_context_data(object_list=object_list, **kwargs)
        context['analytics_html_pages'] = f'analytics/{self.kwargs.get("report_type")}.html'
        context.update({
            'start_date': self.request.GET.get('start_date'),
            'end_date': self.request.GET.get('end_date'),
            'driver': self.request.GET.getlist('driver'),
            'driver_full_name': Driver.objects.all(),
            'report': self.kwargs.get("report_type"),
            'select_driver': select_driver
        }
        )
        return context


class BaseAnalyticsView(BaseDataForAnalytics):
    template_name = 'analytics/analytics_base.html'

    def get_template_name(self, report_type):
        return self.template_dict.get(report_type)

    def get_default_queryset(self, report_type):
        model = self.query_dict.get(report_type, None)
        return model

    def generate_filters(self, *args, driver_filter=None, date_filter=None, **kwargs):
        if driver_filter or date_filter:
            driver_id = self.request.GET.getlist('driver')
            driver_list = self.request.GET.getlist('driver_list')
            if driver_list:
                driver_list = driver_list[0]
                driver_list = ast.literal_eval(driver_list)
                driver_id = driver_list

            start_date = self.request.GET.get('start_date')
            end_date = self.request.GET.get('end_date')
            fil = {}
            if driver_id:
                fil.update({driver_filter: driver_id})
            if start_date and end_date:
                fil.update({date_filter: (start_date, end_date)})

            return fil

        return {}

    def get_filter_dict(self, report_type, *args, **kwargs):
        driver_filter, date_filter = self.filter_dict.get(report_type, (None, None))
        return self.generate_filters(driver_filter=driver_filter, date_filter=date_filter)

    def get_query_filters(self, report_type):
        query_params = self.request.GET
        return self.get_filter_dict(report_type, **query_params)

    def get_queryset(self):
        report_type = self.kwargs.get('report_type')
        queryset = self.get_default_queryset(report_type)
        filters = self.get_query_filters(report_type)
        return queryset.filter(**filters)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        report_type = self.kwargs.get("report_type")
        context['analytics_html_pages'] = f'analytics/{report_type}.html'
        context['report_type'] = report_type
        context['report_type_text'] = report_type.replace('_', ' ').title()
        return context


class CommonAnalyticsView(BaseAnalyticsView, CustomListView):
    extra_context = {
        'form': AnalyticsFilterForm(),
    }


class CommonExportAnalyticsView(BaseAnalyticsView, CustomExportView):

    def get_related_names(self):
        return self.related_names.get(self.kwargs.get('report_type'))
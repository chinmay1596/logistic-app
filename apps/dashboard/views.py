from datetime import date, datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.commons.mixins.commons import LoginAndPermissionMixin
from apps.orders.constants import ACTIVE, UNFULFILLED
from apps.orders.models import Order, OrderBundle
from apps.warehouse.models import WarehouseProduct


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, *args, **kwargs):
        all_orders = Order.objects.all()
        active_order = Order.objects.filter(order_status=ACTIVE)
        till_yesterday_order = Order.objects.filter(order_status=ACTIVE, order_date__lt=date.today()).count()
        unfulfilled_order = Order.objects.filter(order_status=UNFULFILLED).count()
        till_yesterday_unfulfilled_order = Order.objects.filter(order_status=UNFULFILLED,
                                                                order_date__lt=date.today()).count()
        active_bundles = OrderBundle.objects.filter(is_active=True).count()
        till_yesterday_bundle = OrderBundle.objects.filter(is_active=True, created_at__lt=date.today()).count()
        context = super().get_context_data(*args, **kwargs)
        context['active_orders'] = active_order.count()
        context['unfulfilled_orders'] = unfulfilled_order
        context['active_bundles'] = active_bundles
        context['active_increase'] = float(
            ((active_order.count() - till_yesterday_order) / till_yesterday_order) * 100) if till_yesterday_order else 0
        context['active_bundle_increase'] = float(((active_bundles - till_yesterday_bundle) / till_yesterday_bundle)
                                                  * 100) if till_yesterday_bundle else 0
        context['unfulfilled_increase'] = float(((unfulfilled_order - till_yesterday_unfulfilled_order) /
                                                 till_yesterday_unfulfilled_order) * 100) if till_yesterday_unfulfilled_order else 0
        context['recent_orders'] = Order.objects.all().order_by("-id")[:3]
        context['orders_lat_long'] = [list(ele) for ele in
                                      all_orders.values_list('id', 'latitude', 'longitude')] if all_orders else [
            [1, 25.1994, 55.2525]]
        context['low_stocks'] = WarehouseProduct.objects.filter(units__lte=10)[:2]
        context['updates'] = Order.objects.all().order_by("-id")[:3]

        return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
import weasyprint

from apps.commons.mixins.commons import CustomExportView, CustomListView, ListWithFilterAndSearchMixin
from apps.commons.utils.commons import SearchFilter
from apps.commons.utils.pdf import render_to_pdf
from apps.orders.models import Order
from apps.payment.models import Transaction


class PaymentDetailView(ListWithFilterAndSearchMixin):
    template_name = 'payment/payment.html'
    paginate_by = 10
    filter_backends = [SearchFilter]
    search_fields = ['id', 'amount', 'is_paid']
    queryset = Order.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        current_month = datetime.now().month
        context = super().get_context_data(**kwargs)
        outstanding_balance = Order.objects.filter(
            is_paid=False).aggregate(Sum('amount'))
        collected_cash = Order.objects.filter(
            is_paid=True).aggregate(Sum('amount'))
        monthly_earning = Order.objects.filter(
            is_paid=True, created_at__month=current_month)
        context.update(
            {
                "outstanding_balance": outstanding_balance['amount__sum'] if outstanding_balance else 0,
                "collected_cash": collected_cash['amount__sum'] if collected_cash else 0,
                "monthly_earning": monthly_earning.aggregate(Sum('amount'))['amount__sum'] if monthly_earning else 0,
                "orders": Order.objects.all().order_by('-id'),
                "qs": self.request.GET.get("search"),

            }
        )
        return context


def generate_slip(request, transaction_id):
    template = get_template('payment/download.html')
    transaction = get_object_or_404(Transaction, id=transaction_id)
    html = template.render({'transaction': transaction})
    pdf = render_to_pdf('payment/download.html', {'transaction': transaction})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (transaction.transaction_id)
        content = "inline; filename=%s" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


class ExportPaymentView(CustomExportView):
    model = Order
    related_names = {
        'Order Id': 'uuid',
        'Order Date': 'order_date',
        'Customer Name': 'customer.get_full_name',
        'Address': 'address.address',
        'Amount': 'amount',
        # 'Payment Status': 'is_paid',
    }

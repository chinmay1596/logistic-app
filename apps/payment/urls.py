from django.urls import path
from apps.payment.views import PaymentDetailView,generate_slip,ExportPaymentView

app_name = 'payment'
urlpatterns = [
    path('', PaymentDetailView.as_view(), name='payment'),
    path('transaction/<int:transaction_id>/pdf/',generate_slip,name='transaction_pdf'),
    path('export/', ExportPaymentView.as_view(), name='export_payment'),
]

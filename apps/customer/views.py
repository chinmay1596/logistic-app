from django.contrib.messages.views import SuccessMessageMixin
from apps.customer.models import Customer
from django.urls import reverse_lazy
from apps.customer.forms import AddCustomerForm, AddressFormSet
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..commons.mixins.commons import (
    CustomCreateView, ListWithFilterAndSearchMixin, CustomExportView)
from ..commons.utils.commons import SearchFilter
from django.forms import inlineformset_factory
from django.db import transaction


class CustomerListView(ListWithFilterAndSearchMixin):
    queryset = Customer.objects.order_by('-id')
    template_name = 'customer/list.html'
    paginate_by = 7
    filter_backends = [SearchFilter]
    search_fields = ['id', 'first_name',
                     'last_name', 'phone', 'email']


class AddCustomerView(CustomCreateView):
    model = Customer
    form_class = AddCustomerForm
    template_name = 'customer/create.html'
    success_url = reverse_lazy('customer:list')

    def get_context_data(self, **kwargs):
        data = super(AddCustomerView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['address'] = AddressFormSet(self.request.POST)
        else:
            data['address'] = AddressFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        address = context['address']
        with transaction.atomic():
            form.instance.merchant = self.request.user
            self.object = form.save()
            if address.is_valid():
                address.instance.customer = form.instance
                address.instance = self.object
                address.save()

        messages.success(self.request, 'Customer added successfully !')
        return HttpResponseRedirect(self.get_success_url())


class CustomerExport(CustomExportView):
    model = Customer
    related_names = {
        'id': 'id',
        'first_name': 'first_name',
        'phone': 'phone'
    }

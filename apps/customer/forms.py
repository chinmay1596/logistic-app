from apps.customer.models import Customer, Address
from apps.commons.mixins.commons import DynamicFieldsModelForm
from django import forms
from django.forms.models import inlineformset_factory


class AddCustomerForm(DynamicFieldsModelForm):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email', ]

        placeholder = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': ' Email ID',
            'phone': 'Contact Number',
        }


class AddressForm(DynamicFieldsModelForm):
    class Meta:
        model = Address
        fields = ['address_type', 'address']

        placeholder = {
            'address': 'address',
        }


AddressFormSet = inlineformset_factory(
    Customer, Address, form=AddressForm,
    fields=['address_type', 'address'], extra=1, can_delete=True
)
